from django.dispatch import Signal

basic_info_started = Signal(providing_args=[
    "archived_news"])

basic_info_acquired = Signal(providing_args=[
    "archived_news", "time_took"])

basic_info_failed = Signal(providing_args=[
    "archived_news", "error_message"])


internet_archive_started = Signal(providing_args=[
    "archived_news"])

internet_archive_acquired = Signal(providing_args=[
    "archived_news", "time_took"])

internet_archive_failed = Signal(providing_args=[
    "archived_news", "error_message"])


pdf_capture_started = Signal(providing_args=[
    "archived_news"])

pdf_capture_acquired = Signal(providing_args=[
    "archived_news", "pdf_capture", "time_took"])

pdf_capture_failed = Signal(providing_args=[
    "archived_news", "error_message"])
