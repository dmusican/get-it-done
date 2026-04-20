#!/usr/bin/env python3

# Thanks to Claude
import gi
gi.require_version('AyatanaAppIndicator3', '0.1')
gi.require_version('Gtk', '3.0')
from gi.repository import AyatanaAppIndicator3 as AppIndicator3
from gi.repository import Gtk, GLib
import threading
import dbus
from dbus.mainloop.glib import DBusGMainLoop

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
    mode = is_work_mode()
    label = '🔴 Blocked' if mode else '🟢 Unblocked'
    print(f"update called: mode={mode}, label={label}", flush=True)
    indicator.set_label('🔴 Blocked' if is_work_mode() else '🟢 Unblocked', '')
    GLib.timeout_add_seconds(CHECK_INTERVAL, update, indicator)

# def on_resume(indicator):
#     # Re-apply label and restart polling after wake
#     GLib.timeout_add_seconds(10, update, indicator)

def main():
    DBusGMainLoop(set_as_default=True)
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

    # Listen for system resume
    bus = dbus.SystemBus()
    bus.add_signal_receiver(
        # lambda *args: on_resume(indicator),
        lambda *args: GLib.timeout_add_seconds(2, update, indicator),
        signal_name='PrepareForSleep',
        dbus_interface='org.freedesktop.login1.Manager',
        path='/org/freedesktop/login1'
    )

    GLib.timeout_add_seconds(2, update, indicator)  # small delay for startup
    Gtk.main()

if __name__ == '__main__':
    main()
