from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.urls import reverse_lazy
from .owner import *
from .models import Medicine
from .forms import CreateForm
from django.views import View


# for search queries
from django.db.models import Q

# Create your views here.


class MedListView(OwnerListView):
    model = Medicine
    template_name = "medicines/medicine_list.html"

    def get(self, request):
        search = request.GET.get("search", False)
        if search:
            query = Q(name__contains=search)
            # query.add(Q(category__contains=search), Q.OR)
            query.add(Q(description__contains=search), Q.OR)
            medicine_list = Medicine.objects.filter(query).select_related()
        else:
            medicine_list = Medicine.objects.all()
        ctx = {'medicine_list': medicine_list, 'search': search}
        if search:
            ctx['messages'] = ["Showing results for " + search, ]
        return render(request, self.template_name, ctx)


class MedDetailView(OwnerDetailView):
    model = Medicine
    template_name = "medicines/medicine_detail.html"

    # def get(self, request, pk):
    #     x = Medicine.objects.get(id=pk)


class MedCreateView(LoginRequiredMixin, View):
    model = Medicine
    success_url = reverse_lazy("medicines:all")
    template_name = "medicines/medicine_add.html"

    def get(self, request, pk=None):
        form = CreateForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        form = CreateForm(request.POST, request.FILES or None)
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)
        med = form.save(commit=False)
        med.owner = self.request.user
        med.save()
        return redirect(self.success_url)


class MedUpdateView(LoginRequiredMixin, View):
    model = Medicine
    success_url = "medicines:all"
    template_name = "medicines/medicine_add.html"

    def get(self, request, pk):
        med = get_object_or_404(Medicine, id=pk, owner=self.request.user)
        form = CreateForm(instance=med)
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk):
        med = get_object_or_404(Medicine, id=pk, owner=self.request.user)
        form = CreateForm(request.POST, request.FILES or None, instance=med)
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)
        med = form.save(commit=False)
        med.save()
        return redirect(self.success_url)


class MedDeleteView(OwnerDeleteView):
    model = Medicine
    template_name = "medicines/medicine_delete.html"


def stream_file(request, pk):
    med = get_object_or_404(Medicine, id=pk)
    response = HttpResponse()
    if not med.thumbnail: return HttpResponse("No Thumbnail")
    response['Content-Type'] = med.thumb_content_type
    response['Content-Length'] = len(med.thumbnail)
    response.write(med.thumbnail)
    return response

