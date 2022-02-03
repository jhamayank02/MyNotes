from django.shortcuts import render, HttpResponse, redirect
from notes.models import Note
from django.contrib import messages

# Create your views here.
def notes(request):
    allNotes = Note.objects.all().filter(author=request.user).order_by('-timeStamp')
    context = {'allNotes':allNotes}
    return render(request, 'notes.html', context)

def readNote(request, slug):
    note = Note.objects.filter(noteHeading=slug).first()
    context = {'note':note}
    return render(request, 'readNote.html', context)

def addNotes(request):
    if request.method == 'POST':
        author = request.user
        noteHeading = request.POST['noteHeading']
        noteContent = request.POST['noteContent']
        tag = request.POST['tag']
        deadlineDate = request.POST['deadlineDate']
        deadlineTime = request.POST['deadlineTime']
        deadlineTime = request.POST['deadlineTime']

        try:
            if deadlineDate == "" and deadlineTime == "":
                addNote = Note(author=author, noteHeading=noteHeading, noteContent=noteContent, tag=tag)

            elif deadlineDate == "":
                addNote = Note(author=author, noteHeading=noteHeading, noteContent=noteContent, tag=tag, deadlineTime=deadlineTime)

            elif deadlineTime == "":
                addNote = Note(author=author, noteHeading=noteHeading, noteContent=noteContent, tag=tag, deadlineDate=deadlineDate)

            else:
                addNote = Note(author=author, noteHeading=noteHeading, noteContent=noteContent, tag=tag, deadlineDate=deadlineDate, deadlineTime=deadlineTime)

            addNote.save()

            messages.success(request, "Your note has been added successfully")

        except Exception as e:
            messages.error(request, f"{e}")

        return redirect('/notes')
    
    else:
        return HttpResponse('404 - Not Found')

def deleteNote(request):
    if request.method == 'POST':
        noteId = request.POST['noteId']

        Note.objects.filter(sno=noteId).delete()
        messages.success(request, "The note has been deleted successfully")
    
        return redirect('/notes')
    else:
        return HttpResponse('404 - Not Found')
        