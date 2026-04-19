#!/usr/bin/env python3

# Thanks to Claude
import gi
gi.require_version('AyatanaAppIndicator3', '0.1')
gi.require_version('Gtk', '3.0')
from gi.repository import AyatanaAppIndicator3 as AppIndicator3
from gi.repository import Gtk, GLib
import threading

HOSTS_FILE = '/etc/hosts'
START_TOKEN = '## start-gsd'
CHECK_INTERVAL = 5

def is_work_mode():
    try:
        with open(HOSTS_FILE, 'r') as f:
            return START_TOKEN in f.read()
    except:
        return False

def update(indicator):
    indicator.set_label('🔴 Blocked' if is_work_mode() else '🟢 Unblocked', '')
    GLib.timeout_add_seconds(CHECK_INTERVAL, update, indicator)

def main():
    indicator = AppIndicator3.Indicator.new(
        'get-it-done-indicator',
        'dialog-information',
        AppIndicator3.IndicatorCategory.APPLICATION_STATUS
    )
    indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)

    menu = Gtk.Menu()
    quit_item = Gtk.MenuItem(label='Quit')
    quit_item.connect('activate', lambda _: Gtk.main_quit())
    menu.append(quit_item)
    menu.show_all()
    indicator.set_menu(menu)

    GLib.timeout_add_seconds(1, update, indicator)  # small delay for startup
    Gtk.main()

if __name__ == '__main__':
    main()
