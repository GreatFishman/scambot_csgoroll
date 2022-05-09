import time
import asyncio
import sys, os
import multiprocessing as mp
from xml.dom import DOMException
import fuckcaptcha
from pyppeteer import launch


MAIN = 'https://www.csgoroll.com/en/withdraw/csgo/p2p'

async def crawlerFunction():
    try:
        print("...")
        browser = await launch(headless=False, 
                                executablePath='/usr/bin/google-chrome', #'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
                                userDataDir='/home/rene/.config/google-chrome/Default',       #C:\\Users\\Rene-Desktop\\AppData\\Local\\Google\\Chrome\\User
                                args=['--no-sandbox'])
        page = await browser.newPage()
        await fuckcaptcha.bypass_detections(page)
        await page.setViewport({'width': 1072, 'height': 768})
        await page.goto(MAIN)
        print("crawler started. gathering data")
        await asyncio.sleep(3)
        items = []
        blacklist = []
        ##setup page
        #await page.evaluate('''() => { 
        #    document.querySelector("input[formControlName='minValue']").focus()
        #    }''')
        #await page.keyboard.press('1')
        #await page.keyboard.press('5')
        await page.evaluate('''() => { 
            document.querySelector("input[formControlName='maxValue']").focus()
            }''')
        await page.keyboard.press('3')
        await asyncio.sleep(5)
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
            filteredItems = [item for item in items if item not in blacklist]
            for item in filteredItems:
                clickString = "//*[contains(text(),'" + item + "')]"
                footer = await page.Jx(clickString)

                if(len(footer) > 0):
                    await footer[0].click() #footer is a list, take first element
                    await asyncio.sleep(1)
                    withdrawButton = await page.Jx("//*[contains(text(),'Withdraw')]")
                    await withdrawButton[1].click() #2 elements with withdraw as text exist on the page
                    await asyncio.sleep(5)
                    captchaFrame = page.frames[1] #375,470
                    await page.mouse.click(330,390)
                    #await captchaFrame.waitForSelector('div[class="recaptcha-checkbox-border"')
                    #await captchaFrame.click('div[class="recaptcha-checkbox-border"')

                    userInput = ""
                    while(userInput != "y" and userInput != "n"):
                        userInput = input("Move " + item + " to blacklist? [y/n]: ")
                        if(userInput == "y"):
                            print("blacklisting..")
                            blacklist.append(item)
                            #sidebarString = "//cw-selected-sidebar-items[@class='ng-star-inserted']"
                            #selectedSidebar = await page.Jx(sidebarString)
                            #selectedItem =  await selectedSidebar.Jx(clickString)
                            #selectedItem[0].click()
                        elif(userInput == "n"):
                            continue
                        else:
                            print("input y/n only")
            ##end while
    except DOMException as e:
        print(print(sys.exc_info()[0]))


if __name__ == '__main__':
    print("starting crawler...")
    asyncio.run(crawlerFunction())