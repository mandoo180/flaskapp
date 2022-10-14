from flask import render_template, redirect, request, url_for, flash
from app.admin import admin
from app.decorators import admin_required


@admin.route('/')
@admin_required
def index():
    return render_template('admin/index.html')

@admin.route('/products')
@admin_required
def products():
    return render_template('admin/products.html')
