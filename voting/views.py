from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import DeleteView
from django.urls import reverse_lazy, reverse
from .models import Voting, Choice, Vote
from .forms import VotingForm, ChoiceFormSet

@login_required
def voting_list(request):
    votings = Voting.objects.filter(is_active=True)
    return render(request, 'voting/voting_list.html', {'votings': votings})

@login_required
def voting_create(request):
    if request.method == 'POST':
        form = VotingForm(request.POST)
        formset = ChoiceFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            voting = form.save(commit=False)
            voting.creator = request.user
            voting.save()
            
            choices = formset.save(commit=False)
            for choice in choices:
                choice.voting = voting
                choice.save()
            
            messages.success(request, 'Голосование создано!')
            return redirect('voting:list')
    else:
        form = VotingForm()
        formset = ChoiceFormSet()
    
    return render(request, 'voting/voting_form.html', {
        'form': form,
        'formset': formset
    })

@login_required
def voting_detail(request, pk):
    voting = get_object_or_404(Voting, pk=pk)
    user_vote = Vote.objects.filter(voting=voting, user=request.user).first()
    
    if request.method == 'POST' and not user_vote:
        choice_id = request.POST.get('choice')
        if choice_id:
            choice = get_object_or_404(Choice, id=choice_id, voting=voting)
            Vote.objects.create(
                voting=voting,
                choice=choice,
                user=request.user
            )
            messages.success(request, 'Ваш голос учтен!')
            return redirect('voting:detail', pk=voting.pk)
            
    return render(request, 'voting/voting_detail.html', {
        'voting': voting,
        'user_vote': user_vote
    })

class VotingDeleteView(DeleteView):
    model = Voting
    template_name = 'voting/voting_confirm_delete.html'
    success_url = reverse_lazy('voting:list')