import json
from pprint import pprint
from flask import Blueprint, render_template, request, redirect, url_for

books_chapters = {'Genesis': 50, 'Exodus': 40, 'Leviticus': 27, 'Numbers': 36, 'Deuteronomy': 34, 'Joshua': 24, 'Judges': 21, 'Ruth': 4, '1 Samuel': 31, '2 Samuel': 24, '1 Kings': 22, '2 Kings': 25, '1 Chronicles': 29, '2 Chronicles': 36, 'Ezra': 10, 'Nehemiah': 13, 'Esther': 10, 'Job': 42, 'Psalms': 150, 'Proverbs': 31, 'Ecclesiastes': 12, 'Song of Solomon': 8, 'Isaiah': 66, 'Jeremiah': 52, 'Lamentations': 5, 'Ezekiel': 48, 'Daniel': 12, 'Hosea': 14, 'Joel': 3, 'Amos': 9, 'Obadiah': 1, 'Jonah': 4, 'Micah': 7, 'Nahum': 3, 'Habakkuk': 3, 'Zephaniah': 3, 'Haggai': 2, 'Zechariah': 14, 'Malachi': 4, 'Matthew': 28, 'Mark': 16, 'Luke': 24, 'John': 21, 'Acts': 28, 'Romans': 16, '1 Corinthians': 16, '2 Corinthians': 13, 'Galatians': 6, 'Ephesians': 6, 'Philippians': 4, 'Colossians': 4, '1 Thessalonians': 5, '2 Thessalonians': 3, '1 Timothy': 6, '2 Timothy': 4, 'Titus': 3, 'Philemon': 1, 'Hebrews': 13, 'James': 5, '1 Peter': 5, '2 Peter': 3, '1 John': 5, '2 John': 1, '3 John': 1, 'Jude': 1, 'Revelation': 22}

bp = Blueprint('kjv_bible', __name__)

@bp.route("/kjv_bible", methods=['GET', 'POST'])
def index():
    f = open('app/kjv_bible/kjv.json')
    kjv = json.loads(f.read())
    f.close()
    kjv_meta = kjv["metadata"]
    kjv_verses = kjv["verses"]
    book_selected = "Choose a book"
    chapter_selected = '-'
    chapter_list = ['-']
    filtered_verses = [{'-':''}]
    if request.method == "POST":
        book_selected = request.form['book-name']
        # chapter_list = [i for i in range(1, books_chapters[book_selected] + 1)]
        # chapter_selected = request.form['chapter-select']
        # print(f"Book: {book_selected} | Chapter_list: {chapter_list}\n Chapter Selected: {chapter_selected}")
        filtered_verses = [verse_meta for verse_meta in kjv_verses if verse_meta['book_name'] == book_selected]
        # return redirect(url_for('kjv_bible.index'))
        return render_template(
            'kjv_bible/kjv_bible.html', chapter_selected=chapter_selected, book_selected=book_selected, 
            chapter_list=chapter_list, books_chapters=books_chapters, metadata=kjv_meta, verses=filtered_verses
            )
    
    return render_template(
        'kjv_bible/kjv_bible.html', chapter_selected=chapter_selected, book_selected=book_selected, 
        chapter_list=chapter_list, books_chapters=books_chapters, metadata=kjv_meta, verses=filtered_verses
        )