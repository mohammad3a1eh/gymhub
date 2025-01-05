from django.shortcuts import render, redirect
from .forms import PurchaseRequestForm
from django.shortcuts import get_object_or_404
import os
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import PurchaseRequest

@login_required
def create_request(request):
    existing_requests = PurchaseRequest.objects.filter(user=request.user, is_approved=False)
    if existing_requests.exists():
        form = PurchaseRequestForm()
        return render(request, 'shop/create_request.html', {'message': 'You already have a pending request.','form': form})
    
    if request.method == 'POST':
        form = PurchaseRequestForm(request.POST)
        if form.is_valid():
            purchase_request = form.save(commit=False)
            purchase_request.user = request.user
            purchase_request.save()

            # request.session['purchase_request'] = purchase_request.id
            
            return redirect('home')
    else:
        form = PurchaseRequestForm()
    return render(request, 'shop/create_request.html', {'form': form})



@login_required
def upload_program(request, request_id):
    purchase_request = get_object_or_404(PurchaseRequest, id=request_id)
    if not request.user.is_staff:
        return redirect('home')
    
    if request.method == 'POST' and 'program_file' in request.FILES:
        purchase_request.program_file = request.FILES['program_file']
        purchase_request.is_approved = True
        purchase_request.save()
        return redirect('home')

    return render(request, 'shop/upload_program.html', {'purchase_request': purchase_request})



@login_required
def secure_file_download(request, request_id):
    purchase_request = get_object_or_404(PurchaseRequest, id=request_id, user=request.user)
    
    if not purchase_request.is_paid or not purchase_request.is_approved:
        return HttpResponseForbidden("You are not authorized to download this file.")
    
    print(f"Program file name: {purchase_request.program_file.name}")
    print(f"SECURE_FILES_ROOT: {settings.BASE_DIR}")
    
    file_path = os.path.join(settings.BASE_DIR, purchase_request.program_file.name)
    print(f"Complete file path: {file_path}")
    print(f"File exists: {os.path.exists(file_path)}")
    
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/octet-stream")
            response['Content-Disposition'] = f'attachment; filename={os.path.basename(file_path)}'
            return response
    raise Http404("File not found.")
