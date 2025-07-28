from .literature_review_class import *
from .article_class_v2 import *
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from .detection_utils import plagiarism_detection
from tenacity import retry, stop_after_attempt, wait_exponential
#backoff & retry implementation

def Literature_with_retry(self,request):
     data = JSONParser().parse(request)
     print(data)
     style = data.get('style', None)
     researches = data.get('Researches', [])
     subject = data.get('subject', None)
     print(researches)
     res = []
     for i in researches:
          r = Research(i['title'],i['authors'],i['pdf_url'],i['abstract'],i['published'])
          #r = Research(i['title'],i['author'],i['pdfLink'],i['publish_year'])
          res.append(r)
     print(res)
     lr = Literature_Review(res,subject)
     lr.add_citations(style)
     lr.add_references(style)
     return lr.full_literature_review

class LiteratureView(APIView):
     ''' req: (researches:list[dict],style:,subject:str)
      list[i]:{'title':,'authors':,'pdf_url':,'published':},
      style: apa,ieee,mla,ama,asa,aaa,apsa,mhra,oscola
       note: style can not be small 
       subject:the main title of the literature
      (res,201): literature_review: str '''
     @csrf_exempt
     def post(self, request):
        try:
            lr = Literature_with_retry(self,request)
          
            return Response(lr, status=201)
        except Exception as ve:
            return JsonResponse({'detail': str(ve)}, status=500)
#backoff & retry implementation
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def document_with_retry(self, request, *args, **kwargs):
     data = JSONParser().parse(request)
     style = data.get('style', None)
     researches = data.get('Researches', [])
     res = []
     for i in researches:
           r = Research(i['title'],i['authors'],i['pdf_url'],'',i['published'])
           res.append(r)
     ref = documentation(res,style)
     return ref
class Documentation(APIView):
    ''' req: (researches:list[dict],style:str)
      list[i]:{'title':,'authors':,'pdf_url':,'published':},
      style: apa,ieee,mla,ama,asa,aaa,apsa,mhra,oscola
       note: style can not be small letters
      (res,201): literature_review: str '''
    @csrf_exempt
    def post(self, request, *args, **kwargs):
              try:
                  ref = document_with_retry(self,request, *args, **kwargs)
                  return Response(ref['bibstr'], status=201)
                      
              except Exception as ex:
                      return JsonResponse({'detail': str(ex)}, status=500)
#backoff & retry implementation  
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def check_with_retry(self, request, *args, **kwargs):
    data = JSONParser().parse(request)
    text = data.get('text', None)
    token = data.get('token', None)
    status  = plagiarism_detection(text,token)
    return status
class Plagiarism_detector(APIView):
    ''' req: (text:str), (token:str)
      (res,201): status:str,check_result:json via webhook '''
    @csrf_exempt
    def post(self, request):
        try:
           status = check_with_retry(self,request)
           return Response(status, status=201)
        except Exception as ex:
            return JsonResponse({'detailx': str(ex)}, status=500)
#backoff & retry implementation
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def article_with_retry(self, request, *args, **kwargs):
     data = JSONParser().parse(request)
     topic = data.get('topic', None)
     res = data.get('res', None)
     outline = data.get('outline', None)
     arxiv = data.get('arxiv', None)
     print(res)
     ref = article(topic,res,outline,arxiv)
     return ref.final_article
class Article(APIView):
    ''' req: (topic:string,res:list[dict],outline:string,arxiv:boolean),
      (res,201): article: str '''
    @csrf_exempt
    def post(self, request, *args, **kwargs):
              try:
                  res = article_with_retry(self,request, *args, **kwargs)
                  return Response(res, status=201)
                      
              except Exception as ex:
                      return JsonResponse({'detail': str(ex)}, status=500)
#backoff & retry implementation
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def outline_with_retry(self, request, *args, **kwargs):
     data = JSONParser().parse(request)
     topic = data.get('topic', None)
     res = data.get('res', None)
     print(res)
     ref = outline(topic,res)
     return ref
class Outline(APIView):
    ''' req: (topic:string,res:list[dict]),
      (res,201): outline: str '''
    @csrf_exempt
    def post(self, request, *args, **kwargs):
              try:
                  res = outline_with_retry(self,request, *args, **kwargs)
                  return Response(res, status=201)
              except Exception as ex:
                      return JsonResponse({'detail': str(ex)}, status=500)
#backoff & retry implementation
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def complete_with_retry(self, request, *args, **kwargs):
     data = JSONParser().parse(request)
     statement = data.get('statement', None)
     print(statement)
     ref = AutoComplete(statement)
     print(ref)
     return ref.final
class Complete(APIView):
    ''' req: (statement:string,res:list[dict]),
      (res,201): completed: str '''
    @csrf_exempt
    def post(self, request, *args, **kwargs):
              try:
                  res = complete_with_retry(self,request, *args, **kwargs)
                  return Response(res, status=201)
              except Exception as ex:
                      return JsonResponse({'detail': str(ex)}, status=500)
