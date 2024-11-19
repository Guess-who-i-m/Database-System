/**
 * @author See Contributors.txt for code contributors and overview of BadgerDB.
 *
 * @section LICENSE
 * Copyright (c) 2012 Database Group, Computer Sciences Department, University of Wisconsin-Madison.
 */

#include <memory>
#include <iostream>
#include "buffer.h"
#include "exceptions/buffer_exceeded_exception.h"
#include "exceptions/page_not_pinned_exception.h"
#include "exceptions/page_pinned_exception.h"
#include "exceptions/bad_buffer_exception.h"
#include "exceptions/hash_not_found_exception.h"

namespace badgerdb { 

BufMgr::BufMgr(std::uint32_t bufs)					// 构造函数接受一个参数 bufs，它表示缓冲区中缓存的页数。
	: numBufs(bufs) {								// 初始化numBufs：numBufs(bufs) 语句将构造函数传入的 bufs 值赋给成员变量 numBufs，它表示缓冲区的大小。
	bufDescTable = new BufDesc[bufs];				// 分配一块大小为 bufs 的内存，用来存储缓冲区的描述符（BufDesc）。这些描述符包含了每个缓冲区的信息，比如是否有效、页帧编号等。

  	for (FrameId i = 0; i < bufs; i++) 				// 通过一个循环遍历每个缓冲区描述符，为每个缓冲区描述符初始化其属性：
  	{
  		bufDescTable[i].frameNo = i;					// 设置每个缓冲区的帧编号为从 0 到 bufs-1 的值。
  		bufDescTable[i].valid = false;					// 将每个缓冲区的有效性标志设为 false，表示这些缓冲区目前不包含有效数据。
  	}

  	bufPool = new Page[bufs];							// 分配一块内存，大小为 bufs，用来存储缓冲池（bufPool），每个元素是一个 Page 类型的对象，代表缓冲池中的一页数据。

  	int htsize = ((((int) (bufs * 1.2))*2)/2)+1;		// 计算哈希表的大小，基于 bufs 的 1.2 倍大小，并进行一些四舍五入的计算，确保哈希表的大小足够处理缓冲区映射。
  	hashTable = new BufHashTbl (htsize);  			// 分配哈希表内存，用于存储缓冲区的映射信息。

  	clockHand = bufs - 1;								// 将 clockHand 初始化为 bufs - 1，这是一个循环指针，用于实现时钟页面替换算法。它表示缓冲区的起始位置。
}

// BufMgr中的析构函数。将缓冲池中的所有脏页写回磁盘，然后释放缓冲区，BufDesc表和Hash表占用的内存
BufMgr::~BufMgr() {
	// 遍历整个缓冲区
	for (FrameId i = 0; i < numBufs; i ++) {
		if (bufDescTable[i].dirty == true && bufDescTable[i].valid){
			// 将脏页写回
			bufDescTable[i].file->writePage(bufPool[i]);
		}
	}

	// 释放缓冲区
	if (bufPool) delete[] bufPool;
	if (bufDescTable) delete[] bufDescTable;
	if (hashTable) delete hashTable;
}

// 顺时针旋转时钟算法的表针，让其转向缓冲池中的下一个页框
void BufMgr::advanceClock()
{
	clockHand = (clockHand + 1) % numBufs;//由于总体的缓冲池是一个环形结构，所以对页框编号+1后要再去模缓冲区大小
}

// 使用时钟算法分配一个空闲的页框，
// 如果页框中的页面是脏的，先将脏页写回磁盘
// 如果缓冲池中所有页面都被固定住了pinned，抛出BufferExceededException异常
// 如果被分配页框中包含了一个有效页面，将页面从哈希表中也删除。分配的页框编号通过frame返回
void BufMgr::allocBuf(FrameId & frame) 
{
	// 先检查是否所有页面全被pinned住了
	int pinnedPageCount = 0;
	for (FrameId i =0; i < numBufs; i ++){
		if (bufDescTable[i].pinCnt > 0){
			pinnedPageCount ++;
		}
	}

	if (pinnedPageCount == numBufs){
		throw BufferExceededException();
	}

	// 确定好了并非所有页面都被固定住，进行正常的算法分配
	while(true){

		advanceClock();	// 先让时针走向下一个界面

		if (bufDescTable[clockHand].valid == false) {
			// 如果页面本来无效，说明空闲，可以直接赋给它
			frame = clockHand;
			return;
		}

		// 看页面是否最近被访问过
		if (bufDescTable[clockHand].refbit== true){
			bufDescTable[clockHand].refbit = false;
			continue;		// 最近被访问过，清空refbit位然后跳过这轮循环
		}

		// 判断页面是否被固定
		if (bufDescTable[clockHand].pinCnt > 0){
			continue;
		}

		// 看是否设置了脏位，如果设置了脏位需要先写回
		if (bufDescTable[clockHand].dirty == true){
			bufDescTable[clockHand].file->writePage(bufPool[clockHand]);
			bufDescTable[clockHand].dirty = false;
		}

		try{
			hashTable->remove(bufDescTable[clockHand].file, bufDescTable[clockHand].pageNo);
		}
		catch(HashNotFoundException e){

		}

		bufDescTable[clockHand].Clear();
		frame = clockHand;
		return;
	}
}


// 调用哈希表的lookup方法检查待读取的页面是否已经在缓冲池中
//   若页面在缓冲池中，通过page返回指向页面所在的页框的指针
//   若也页面不在缓冲池中，抛出HashNotFound异常
// 根据lookup方法的结果，处理两种情况
//   页面不在缓冲池中，调用allocBuf分配一个空闲的页框，随后调用file->readPage()方法将页面从磁盘读入到页框中
//     随后将页面插入到Hash表中，调用Set方法设置页框的状态，Set将页面的pinCnt设置为1，最后用page返回指向页框的指针
//   页面在缓冲池中，将页框的refbit设置为true，将pinCnt加1，最后通过page返回指向页框的指针
void BufMgr::readPage(File* file, const PageId pageNo, Page*& page)
{
	FrameId frameNo;

	try{
		hashTable->lookup(file, pageNo, frameNo);
		bufDescTable[frameNo].refbit = true;
		bufDescTable[frameNo].pinCnt ++;
		page = bufPool + frameNo;					//这里注意，重要的不是返回页面内容，而是页面地址
	}
	catch (HashNotFoundException e){
		allocBuf(frameNo);
		bufPool[frameNo] = file->readPage(pageNo); // 从文件读取内容出来
		hashTable->insert(file, pageNo, frameNo);
		bufDescTable[frameNo].Set(file, pageNo);
		page = bufPool + frameNo;
	}

	return;
}

// 将缓冲区中所有包含了(file, pageNo)表示的页面所在页框的pinCnt-1
// 如果参数dirty为1，则对应将页框的dirty位设置为1
// 如果pinCnt已经设置为0，那么抛出PAGENOPINNED异常。
// 如果页面不在哈希表中，那么啥也不做
void BufMgr::unPinPage(File* file, const PageId pageNo, const bool dirty) 
{
	// 通过Hash表查询frameNo
	FrameId frameNo;
	try{
		hashTable->lookup(file, pageNo, frameNo);

		if (bufDescTable[frameNo].pinCnt > 0){
			bufDescTable[frameNo].pinCnt --;
		} else {
			throw PageNotPinnedException(bufDescTable[frameNo].file->filename(), bufDescTable[frameNo].pageNo, frameNo);
		}
		
		if ( dirty == true){
			bufDescTable[frameNo].dirty = true;
		}

	}
	catch(HashNotFoundException e){
		// 什么都不做
	}
}

// 扫描bufTable，检索缓冲区中所有属于文件file的页面。对于每个检索到的页面：
// 如果页面是脏的，调用file->writePage()将页面写回磁盘，并且将dirty位设置为false
// 将页面从哈希表中删除
// 调用BufDesc类的Clear()方法，将页框的状态重置
// 两种异常情况：
//   如果file的某些页面固定住，那么抛出BadBufferException异常
//   如果file的的页面无效，那么也抛出BadBufferException异常
void BufMgr::flushFile(const File* file) 
{
	for (FrameId i = 0; i < numBufs; i ++){
		
		if (bufDescTable[i].file == file){

			if (bufDescTable[i].pinCnt > 0){
				// printf("first\n");
				// throw BadBufferException(i, bufDescTable[i].dirty, bufDescTable[i].valid, bufDescTable[i].refbit );
				throw PagePinnedException(bufDescTable[i].file->filename(), bufDescTable[i].pageNo, i);
			}

			if (bufDescTable[i].valid == false){
				// printf("second\n");
				throw BadBufferException(i, bufDescTable[i].dirty, bufDescTable[i].valid, bufDescTable[i].refbit );
			}

			if (bufDescTable[i].dirty == true){
				bufDescTable[i].file->writePage(bufPool[i]);
				bufDescTable[i].dirty = false;
			}

			hashTable->remove(file, bufDescTable[i].pageNo);

			bufDescTable[i].Clear();
		}
	}
}

// 首先调用file->allocatePage()方法在file文件中分配一个空闲页面，方法会返回这个新分配的页面
// 调用allocBuf方法在缓冲区分配一个空闲的页框
// 在哈希表中插入一条项目，在调用Set()方法正确设置页框状态，Set方法通过pageNo返回新分配的页面的页号
// 通过page参数返回指向缓冲区中包含这个页面的页框的指针
void BufMgr::allocPage(File* file, PageId &pageNo, Page*& page) 
{
	FrameId frameNo;
	Page pageContent;
	// 首先分配一个空闲页面
	pageContent = file->allocatePage();
	// 随后分配一个空闲的页框
	allocBuf(frameNo);
	bufPool[frameNo] = pageContent;
	pageNo = pageContent.page_number();     // 通过page_number()方法获取页在file中的页号
	// 随后在哈希表中插入信息，在描述符表中补全信息
	hashTable->insert(file, pageNo, frameNo);
	bufDescTable[frameNo].Set(file, pageNo);

	page = bufPool + frameNo;
}

// 从文件file中删除页号为pageNo的页面
// 在删除之前，如果页面在缓冲池中，需要将该页面所在的页框清空，并且从哈希表中删除这个页面
void BufMgr::disposePage(File* file, const PageId PageNo)
{
	for (FrameId i = 0; i < numBufs; i ++) {
		if (bufDescTable[i].file == file && bufDescTable[i].pageNo == PageNo){
			bufDescTable[i].Clear();
			hashTable->remove(file, PageNo);
		}
	}

    file->deletePage(PageNo);
}

void BufMgr::printSelf(void) 
{
  BufDesc* tmpbuf;
	int validFrames = 0;
  
  for (std::uint32_t i = 0; i < numBufs; i++)
	{
  	tmpbuf = &(bufDescTable[i]);
		std::cout << "FrameNo:" << i << " ";
		tmpbuf->Print();

  	if (tmpbuf->valid == true)
    	validFrames++;
  }

	std::cout << "Total Number of Valid Frames:" << validFrames << "\n";
}

}
