from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Article, Manual, Product, Photo
from .forms import ArticleForm, ManualForm, ProductForm, ArticleDeleteForm, PhotoForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home(request):
    manual_list = Manual.objects.all()
    product_list = Product.objects.all()

    return render(
        request,
        "support/home.html",
        {"manual_list": manual_list, "product_list": product_list},
    )


def manual_detail(request, manual_pk):
    manual = get_object_or_404(Manual, pk=manual_pk)

    article_list = Article.objects.filter(manual_name=manual, available=True).order_by(
        "ordery", "orderx"
    )
    product_list = Product.objects.all()
    manual_list = Manual.objects.all()
    return render(
        request,
        "support/manual_detail.html",
        {
            "manual": manual,
            "article_list": article_list,
            "product_list": product_list,
            "manual_list": manual_list,
        },
    )


def manual_update(request, pk):
    if request.method == "POST":
        manual = get_object_or_404(Manual, pk=pk)
        form = ManualForm(request.POST, request.FILES, instance=manual)
        if form.is_valid():
            form.save()
            return redirect("support:home")
    else:
        manual = get_object_or_404(Manual, pk=pk)
        form = ManualForm(instance=manual)
    return render(request, "support/manual_form.html", {"form": form})


def manual_reorder(request, manual_pk):
    product_list = Product.objects.all()
    manual_list = Manual.objects.all()

    manual = get_object_or_404(Manual, pk=manual_pk)
    article_list = Article.objects.filter(manual_name=manual, available=True).order_by(
        "ordery", "orderx"
    )
    i = 1
    btw_number = 64
    for article in article_list:
        instance = get_object_or_404(Article, pk=article.pk)
        instance.ordery = i * btw_number
        instance.save()
        i += 1

    return render(
        request,
        "support/manual_detail.html",
        {
            "manual": manual,
            "article_list": article_list,
            "product_list": product_list,
            "manual_list": manual_list,
        },
    )


def article_list(request, pk):
    article_list = Article.objects.filter(available=True)
    product_list = Product.objects.all()
    manual_list = Manual.objects.all()
    manual = get_object_or_404(Manual, pk=pk)
    paginator = Paginator(article_list, 10)  # Show 10 articles per page

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "support/article_list.html",
        {
            "page_obj": page_obj,
            "product_list": product_list,
            "manual_list": manual_list,
            "manual": manual,
        },
    )


def article_create(request, manual_pk):
    product_list = Product.objects.all()
    manual_list = Manual.objects.all()
    manual = get_object_or_404(Manual, pk=manual_pk)
    first_ordery = (
        Article.objects.filter(manual_name=manual).order_by("-ordery").first()
    )
    new_ordery = first_ordery.ordery + 64

    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.instance.manual_name = manual
            form.instance.user = request.user  # Set the user of the new Article
            form.instance.ordery = new_ordery
            form.save()
            return redirect("support:manual-detail", manual_pk=manual_pk)
    else:
        form = ArticleForm(initial={"manual_pk": manual_pk})
    return render(
        request,
        "support/article_create.html",
        {
            "form": form,
            "product_list": product_list,
            "manual_list": manual_list,
            "manual": manual,
        },
    )


def manual_create_btw(request, manual_pk, article_pk, article_ordery, article_orderx):
    product_list = Product.objects.all()
    manual_list = Manual.objects.all()
    manual = get_object_or_404(Manual, pk=manual_pk)
    article = get_object_or_404(Article, pk=article_pk)

    new_ordery = article_ordery - 4

    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.instance.manual_name = manual
            form.instance.user = request.user  # Set the user of the new Article
            form.instance.ordery = new_ordery
            form.instance.orderx = article.orderx + 1
            form.save()
            return redirect("support:manual-detail", manual_pk=manual_pk)
    else:
        form = ArticleForm(initial={"ordery": new_ordery, "orderx": article_orderx + 1})
    return render(
        request,
        "support/article_create_btw.html",
        {
            "form": form,
            "product_list": product_list,
            "manual_list": manual_list,
            "manual": manual,
            "article_ordery": article_ordery,
        },
    )


def article_detail(request, manual_pk, article_pk):
    product_list = Product.objects.all()
    manual_list = Manual.objects.all()
    manual = get_object_or_404(Manual, pk=manual_pk)

    if request.method == "GET":
        article = get_object_or_404(Article, pk=article_pk)
        return render(
            request,
            "support/article_detail.html",
            {
                "article": article,
                "manual": manual,
                "product_list": product_list,
                "manual_list": manual_list,
            },
        )
    else:
        return HttpResponse("Method Not Allowed", status=405)


def article_update(request, manual_pk, article_pk):
    product_list = Product.objects.all()
    manual_list = Manual.objects.all()
    manual = get_object_or_404(Manual, pk=manual_pk)
    article = get_object_or_404(Article, pk=article_pk)

    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.instance.user = request.user  # Set the user of the new Article
            form.save()
            return redirect(
                "support:article-detail", manual_pk=manual_pk, article_pk=article_pk
            )
    else:
        form = ArticleForm(instance=article)
    return render(
        request,
        "support/article_update.html",
        {
            "form": form,
            "article": article,
            "manual": manual,
            "product_list": product_list,
            "manual_list": manual_list,
        },
    )


def article_delete(request, manual_pk, article_pk):
    product_list = Product.objects.all()
    manual_list = Manual.objects.all()
    manual = get_object_or_404(Manual, pk=manual_pk)
    article = get_object_or_404(Article, pk=article_pk)

    if request.method == "POST":
        form = ArticleDeleteForm(request.POST, instance=article)
        if form.is_valid():
            article.available = False
            article.save()

            return redirect("support:manual-detail", manual_pk=manual_pk)

    else:
        form = ArticleDeleteForm(instance=article)

    return render(
        request,
        "support/article_delete.html",
        {
            "form": form,
            "article": article,
            "manual": manual,
            "product_list": product_list,
            "manual_list": manual_list,
        },
    )


def photo_list(request):
    product_list = Product.objects.all()
    manual_list = Manual.objects.all()
    photos = Photo.objects.all()
    context = {
        "photos": photos,
        "product_list": product_list,
        "manual_list": manual_list,
    }
    return render(request, "support/photo_list.html", context)


def photo_detail(request, pk):
    return render(request, "support/photo_detail.html")


def photo_create(request):
    user = request.user
    if request.method == "POST":
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = user
            form.save()
            return redirect("support:photo-list")
    else:
        form = PhotoForm()
    return render(request, "support/photo_create.html", {"form": form})


def photo_update(request, pk):
    return render(request, "support/photo_update.html")


def photo_delete(request, pk):
    return render(request, "support/photo_delete.html")
