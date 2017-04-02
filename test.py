# vim: set ts=4 sw=4 et: -*- coding: utf-8 -*-
import unittest
from PttWebCrawler import PttWebCrawler as crawler
import codecs, json, os

class TestCrawler(unittest.TestCase):
    def test_parse(self):
        self.link = 'https://www.ptt.cc/bbs/PublicServan/M.1490923302.A.78F.html'
        self.article_id = 'M.1490923302.A.78F'
        self.board = 'PublicServan'

        c = crawler(board=self.board, iOrA=False, article_id=self.article_id)
        jsondata = json.loads(c.parse(self.link, self.article_id))
        self.assertEqual(jsondata['article_id'], self.article_id)
        self.assertEqual(jsondata['board'], self.board)
        self.assertEqual(jsondata['message_conut']['count'], 3)
    
    def test_parse_with_structured_push_contents(self):
        self.link = 'https://www.ptt.cc/bbs/Gossiping/M.1119222660.A.94E.html'
        self.article_id = 'M.1119222660.A.94E'
        self.board = 'Gossiping'

        c = crawler(board=self.board, iOrA=False, article_id=self.article_id)
        jsondata = json.loads(c.parse(self.link, self.article_id))
        self.assertEqual(jsondata['article_id'], self.article_id)
        self.assertEqual(jsondata['board'], self.board)
        isCatched = False
        for msg in jsondata['messages']:
            if u'http://tinyurl.com/4arw47s' in msg['push_content']:
                isCatched = True
        self.assertTrue(isCatched)

    def test_parse_with_push_without_contents(self):
        self.link = 'https://www.ptt.cc/bbs/Gossiping/M.1433091897.A.1C5.html'
        self.article_id = 'M.1433091897.A.1C5'
        self.board = 'Gossiping'

        c = crawler(board=self.board, iOrA=False, article_id=self.article_id)
        jsondata = json.loads(c.parse(self.link, self.article_id))
        self.assertEqual(jsondata['article_id'], self.article_id)
        self.assertEqual(jsondata['board'], self.board)

    def test_parse_without_metalines(self):
        self.link = 'https://www.ptt.cc/bbs/NBA/M.1432438578.A.4B0.html'
        self.article_id = 'M.1432438578.A.4B0'
        self.board = 'NBA'

        c = crawler(board=self.board, iOrA=False, article_id=self.article_id)
        jsondata = json.loads(c.parse(self.link, self.article_id))
        #print jsondata
        self.assertEqual(jsondata['article_id'], self.article_id)
        self.assertEqual(jsondata['board'], self.board)

    def test_crawler(self):
        crawler(board='PublicServan', iOrA=True, start='1', end='2')
        filename = 'PublicServan-1-2.json'
        with codecs.open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # M.1127808641.A.C03.html is empty, so decrease 1 from 40 articles
            self.assertEqual(len(data['articles']), 39)
        os.remove(filename)
	
    def test_getLastPage(self):
        boards = ['NBA', 'Gossiping', 'b994060work']  # b994060work for 6259fc0 (pull/6)

        for board in boards:
            try:
                c = crawler(board=board, iOrA=False, article_id='M.1432438578.A.4B0')
                _ = c.getLastPage()
            except:
                self.fail("getLastPage() raised Exception.")


if __name__ == '__main__':
    unittest.main()
