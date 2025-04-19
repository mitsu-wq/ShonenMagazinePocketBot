import aiohttp
from bs4 import BeautifulSoup

import json
from .exception import GetChapterFailed
from .utils import sanitize_text, ddir


async def _GetChapter(response: aiohttp.client_reqrep.ClientResponse):
    """Parse chapter data from an HTTP response.

    Extracts title, chapter number, and page URLs from the HTML response.

    Args:
        response (aiohttp.client_reqrep.ClientResponse): The HTTP response object.

    Returns:
        tuple: (title, chapter, pages) where title is the manga title, chapter is the chapter number,
               and pages is a list of page URLs.

    Raises:
        GetChapterFailed: If parsing fails due to missing elements or invalid data.
    """
    text = await response.read()
    ms = BeautifulSoup(text.decode("utf-8"), "lxml")
    
    title_elem = ms.select_one(".series-header-title") or ms.select_one("[class*='series-title']")
    if not title_elem:
        raise GetChapterFailed("Chapter title not found")
    title = sanitize_text(title_elem.text)
    
    chapter_elem = ms.select_one(".episode-header-title") or ms.select_one("[class*='episode-title']")
    if not chapter_elem:
        raise GetChapterFailed("Chapter number not found")
    chapter = sanitize_text(chapter_elem.text)

    prj = ms.select_one("script#episode-json")
    if not prj or not prj.get("data-value"):
        raise GetChapterFailed("Chapter data not found")
    try:
        pd = ddir(json.loads(prj["data-value"]), "readableProduct/pageStructure/pages")
    except json.JSONDecodeError:
        raise GetChapterFailed("Invalid chapter data format")
    pages = [i["src"] for i in pd if i["type"] == "main"]
    if not pages:
        raise GetChapterFailed("No pages found in chapter")

    return title, chapter, pages

async def GetChapter(num: str, email_address: str = None, password: str = None):
    """Fetch manga chapter data from pocket.shonenmagazine.com.

    Performs authentication if credentials are provided and retrieves chapter data.

    Args:
        num (str): Chapter ID.
        email_address (str, optional): User email for login.
        password (str, optional): User password for login.

    Returns:
        tuple: (title, chapter, pages) where title is the manga title, chapter is the chapter number,
               and pages is a list of page URLs.

    Raises:
        GetChapterFailed: If login fails or chapter data cannot be retrieved.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1",
        "X-Requested-With": "XMLHttpRequest"
    }
        
    async with aiohttp.ClientSession("https://pocket.shonenmagazine.com") as session:
        if email_address is not None and password is not None:
            data = {
                "email_address": email_address,
                "password": password
            }
            async with session.post(url="/user_account/login", data=data, headers=headers) as login_response:
                if login_response.status != 200:
                    raise GetChapterFailed("Login failed. Check your credentials.")
                async with session.get(url=f"/episode/{num}", headers=headers) as response:
                    return await _GetChapter(response)
        else:
            async with session.get(url=f"/episode/{num}", headers=headers) as response:
                return await _GetChapter(response)