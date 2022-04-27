import time
import asyncio
import sys, os
import multiprocessing as mp
from pyppeteer import launch


MAIN = 'https://www.csgoroll.com/en/withdraw/csgo/p2p'

async def crawlerFunction():
    try:
        browser = await launch(headless=False, 
                                executablePath='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', 
                                userDataDir="C:\\Users\\Rene-Desktop\\AppData\\Local\\Google\\Chrome\\User",
                                args=['--no-sandbox'])
        page = await browser.newPage()
        await page.goto(MAIN)
        print("crawler started. gathering data")
        await asyncio.sleep(3)
        items = []
        blacklist = []
        ##setup page
        await page.evaluate('''() => { 
            document.querySelector("input[formControlName='minValue']").focus()
            }''')
        await page.keyboard.press('1')
        await page.keyboard.press('5')
        await asyncio.sleep(10)
        ##crawl for items
        while(1):
            items = await page.evaluate('''() => {
                let itemElements = document.getElementsByClassName('item-footer');
                let items = []
                Array.from(itemElements).forEach((item) => {
                    //let brand = item.getElementsByClassName('brand')[0].textContent;
                    let name = item.getElementsByClassName('name')[0].textContent;
                    //fullName = brand + name;
                    items.push(name);
                })
                return items
            }''')
            print("trace")
            filteredItems = [item for item in items if item not in blacklist]
            print("trace1")
            for item in filteredItems:
                print("trace2")
                clickString = 'div[textContent=\'' + item + '\']'
                print(clickString)
                footer = await page.querySelector('div[textContent=\'' + item + '\']')
                print("trace")
                await footer.click()
                print("trace2")
                await page.click(clickString)
                input = input("Move " + item + " to blacklist? y/n")
            ##end while
    except Exception as e:
        print(sys.exc_info()[0])
        raise



def crawlerThread():
    print("starting crawler...")
    asyncio.run(crawlerFunction())

if __name__ == '__main__':
    pool = mp.Pool(mp.cpu_count())
    res1 = pool.apply_async(crawlerThread)
    pool.close()
    pool.join()