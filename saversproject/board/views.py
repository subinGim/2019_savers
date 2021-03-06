from django.shortcuts import get_object_or_404, render, redirect
from .models import NoticeBoard, QABoard, QABoardComment
from .forms import NoticeForm, QAForm, CommentForm
from django.utils import timezone
# from .decorators import login_required, superuser_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

def noticeboard(request):
        notices = NoticeBoard.objects
        usermodel = get_user_model().objects.get(id=request.user.id)
        return render(request, 'board/n_board.html', {'notices':notices, 'user':usermodel})

def qaboard(request):
        questions = QABoard.objects.select_related() #foreign key값을 기준으로 inner join 됨.
        return render(request, 'board/q_board.html', {'questions':questions})

@login_required
def write(request, word):
        return render(request,'board/write.html', {'word':word})
def detail(request):
        return render(request,'board/detail.html')

#공지글 생성 함수
def n_create(request):
        notice = NoticeBoard()
        if request.method == 'POST':
                form = NoticeForm(request.POST, instance=notice)
                notice.title = request.POST['title']
                notice.content = request.POST['content']
                if form.is_valid():
                        notice = form.save(commit=False)
                        notice.pub_date = timezone.datetime.now()
                        notice.save()
                        return redirect('noticeboard')
        else:
                form = NoticeForm(instance=notice)
                return render(request, 'board/write.html', {'form':form})    
#질문글 생성 함수        
def q_create(request):
        question = QABoard()
        if request.method == 'POST':
                form = QAForm(request.POST, instance=question)
                question.title = request.POST['title']
                question.content = request.POST['content']
                if form.is_valid():
                        question = form.save(commit=False)
                        question.pub_date = timezone.datetime.now()
                        question.user_id = request.user.id #현재 로그인 되어 있는 계정의 id값을 가져오기.
                        # username = request.user.name
                        question.save()
                        # return render(request, 'board/q_board.html', {'username':username})
                        return redirect('qaboard')
        else:
                form = QAForm(instance=question)
                return render(request, 'board/write.html', {'form':form})        

#notice 카테고리의 글 내용을 보여줄 함수
def notice_detail(request, noticeboard_id):
        n_detail = get_object_or_404(NoticeBoard, pk=noticeboard_id)
        return render(request, 'board/n_detail.html', {'n_detail':n_detail})

#q&a 카테고리의 글 내용을 보여줄 함수
def QandA_detail(request, qaboard_id):
        q_detail = get_object_or_404(QABoard, pk=qaboard_id)
        length = QABoardComment.objects.filter(q_a_id=qaboard_id).count()

        if length == 1:
                answer = QABoardComment.objects.get(q_a_id=qaboard_id)
        else:
                answer = "No Answer"
        return render(request, 'board/q_detail.html', {'q_detail':q_detail, 'answer':answer})
        # if QABoardComment.objects.get(q_a_id=qaboard_id).exists:
        #         answer = get_object_or_404(QABoardComment, q_a_id=qaboard_id)
        # else:
        #         answer = "No Answer"
        # return render(request, 'board/q_detail.html', {'q_detail':q_detail})
        
# 질문글에 대한 관리자의 댓글 생성
def createAnswer(request, qaboard_id):
        answer = QABoardComment()
        q_detail = get_object_or_404(QABoard, pk=qaboard_id)
        if request.method == 'POST':
                form = CommentForm(request.POST, instance=answer)
                answer.content = request.POST['content']
                if form.is_valid():
                        answer = form.save(commit=False)
                        answer.q_a_id = q_detail.id #현재 로그인 되어 있는 계정의 id값을 가져오기.
                        # username = request.user.name
                        answer.save()
                        # return redirect('QandA_detail')
                        return render(request, 'board/q_detail.html', {'q_detail':q_detail, 'answer':answer})

        else:
                form = CommentForm(instance=answer)
                return render(request, 'board/answer.html', {'form':form, 'q_detail':q_detail})     
        return render()
