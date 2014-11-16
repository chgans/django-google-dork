from django.test import TestCase
from django.db import IntegrityError
from django.core.exceptions import ValidationError

from django_google_dork.models import Campaign, Dork, Run, Result

class TestCampaign(TestCase):

    def setUp(self):
        pass

    def test_name_not_empty(self):
        with self.assertRaises(ValidationError):
            c=Campaign.objects.create(name="")
            c.full_clean()

    def test_name_is_stripped(self):
        c=Campaign.objects.create(name=" test ")
        c.full_clean()
        self.assertEqual(c.name, "test")

    def test_name_is_long_enough(self):
        with self.assertRaises(ValidationError):
            c=Campaign.objects.create(name="t"*3)
            c.full_clean()

    def test_name_is_short_enough(self):
        with self.assertRaises(ValidationError):
            c=Campaign.objects.create(name="t"*33)
            c.full_clean()

    def test_name_is_unique(self):
        with self.assertRaises(IntegrityError):
            Campaign.objects.create(name="test")
            Campaign.objects.create(name="test")

    def test_run_set(self):
        c=Campaign.objects.create(name="campaign")
        d=Dork.objects.create(campaign=c, query="query")
        n=3
        for i in range(n):
            r=Run.objects.create(dork=d)
        self.assertEqual(c.run_set.count(), n)
        self.assertEqual(c.run_set.last(), r)
        self.assertEqual(c.run_set.last(), d.run_set.last())

    def test_result_set(self):
        c=Campaign.objects.create(name="campaign")
        d=Dork.objects.create(campaign=c, query="query")
        r=Run.objects.create(dork=d)
        n=3
        for i in range(n):
            s=Result.objects.create(title="title%d" % (i),
                                    summary="summary",
                                    url="http://some.where/path")
            r.result_set.add(s)
        self.assertEqual(c.result_set.count(), n)
        self.assertEqual(c.result_set.last(), s)
        self.assertEqual(c.result_set.last(), r.result_set.last())

class TestDork(TestCase):

    def setUp(self):
        pass

    def test_campaign_not_null(self):
        with self.assertRaises(IntegrityError):
            d=Dork.objects.create()
            d.full_clean()

    def test_query_not_null(self):
        c=Campaign.objects.create(name="c")
        with self.assertRaises(IntegrityError):
            d=Dork.objects.create(campaign=c, query=None)

    def test_query_not_empty(self):
        c=Campaign.objects.create(name="c")
        with self.assertRaises(ValidationError):
            d=Dork.objects.create(campaign=c, query="")
            d.full_clean()

    def test_query_is_stripped(self):
        c=Campaign.objects.create(name="c")
        d=Dork.objects.create(campaign=c, query=" test ")
        d.full_clean()
        self.assertEqual(d.query, "test")

    def test_query_is_long_enough(self):
        c=Campaign.objects.create(name="c")
        with self.assertRaises(ValidationError):
            d=Dork.objects.create(campaign=c, query="t"*0)
            d.full_clean()

    def test_query_is_short_enough(self):
        c=Campaign.objects.create(name="c")
        with self.assertRaises(ValidationError):
            d=Dork.objects.create(campaign=c, query="t"*257)
            d.full_clean()

    def test_campaign_and_query_00(self):
        c0=Campaign.objects.create(name="c0")
        c1=Campaign.objects.create(name="c1")
        Dork.objects.create(campaign=c0, query="test0")
        Dork.objects.create(campaign=c1, query="test1")

    def test_campaign_and_query_01(self):
        c0=Campaign.objects.create(name="c0")
        c1=Campaign.objects.create(name="c1")
        Dork.objects.create(campaign=c0, query="test")
        Dork.objects.create(campaign=c1, query="test")

    def test_campaign_and_query_10(self):
        c=Campaign.objects.create(name="c")
        Dork.objects.create(campaign=c, query="test0")
        Dork.objects.create(campaign=c, query="test1")

    def test_campaign_and_query_11(self):
        c=Campaign.objects.create(name="c")
        Dork.objects.create(campaign=c, query="test")
        with self.assertRaises(IntegrityError):
            Dork.objects.create(campaign=c, query="test")

    def test_result_set(self):
        c=Campaign.objects.create(name="campaign")
        d=Dork.objects.create(campaign=c, query="query")
        r=Run.objects.create(dork=d)
        for i in range(3):
            s=Result.objects.create(title="title%d" % i,
                                    summary="summary",
                                    url="http://some.where/path")
            r.result_set.add(s)
        self.assertEqual(d.result_set.count(), 3)
        self.assertEqual(d.result_set.last(), s)
        self.assertEqual(d.result_set.last(), r.result_set.last())

class TestRun(TestCase):

    def setUp(self):
        pass

    def test_create_dork_not_empty(self):
        with self.assertRaises(IntegrityError):
            Run.objects.create()

    def test_create_wo_results(self):
        c=Campaign.objects.create(name="campaign")
        d=Dork.objects.create(campaign=c, query="query")
        r=Run.objects.create(dork=d)

    # result_set doen't contains 2 identical result
    # This is actually enforced by Django itself!
    def test_result_uniqness(self):
        c=Campaign.objects.create(name="campaign")
        d=Dork.objects.create(campaign=c, query="query")
        r=Run.objects.create(dork=d)
        s=Result.objects.create(title="title",
                                summary="summary",
                                url="http://some.where/path")
        r.result_set.add(s)
        r.result_set.add(s)
        self.assertEqual(r.result_set.count(), 1)

class TestResult(TestCase):

    def setUp(self):
        pass

    def create_result(self):
        r=Result.objects.create(title="title",
                                 summary="summary",
                                 url="http://some.where/path")
        return r

    def test_uniqness(self):
        r=self.create_result()
        with self.assertRaises(IntegrityError):
            self.create_result()
            
