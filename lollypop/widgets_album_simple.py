# Copyright (c) 2014-2018 Cedric Bellegarde <cedric.bellegarde@adishatz.org>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from gi.repository import GLib, Gtk, Pango, GObject

from gettext import gettext as _

from lollypop.widgets_album import AlbumWidget
from lollypop.helper_overlay import OverlayAlbumHelper
from lollypop.define import App, ArtSize, Shuffle


class AlbumSimpleWidget(Gtk.FlowBoxChild, AlbumWidget, OverlayAlbumHelper):
    """
        Album widget showing cover, artist and title
    """
    __gsignals__ = {
        "populated": (GObject.SignalFlags.RUN_FIRST, None, ()),
        "overlayed": (GObject.SignalFlags.RUN_FIRST, None, (bool,))
    }

    ctx = App().window.get_pango_context()
    layout = Pango.Layout.new(ctx)
    layout.set_text("a", 1)
    # * 2 => two labels
    LABEL_HEIGHT = int(layout.get_pixel_size()[1])

    def __init__(self, album, genre_ids, artist_ids):
        """
            Init simple album widget
            @param album as Album
            @param genre ids as [int]
            @param artist_ids as [int]
        """
        self.__widget = None
        # We do not use Gtk.Builder for speed reasons
        Gtk.FlowBoxChild.__init__(self)
        self.set_size_request(ArtSize.BIG, ArtSize.BIG + self.LABEL_HEIGHT)
        AlbumWidget.__init__(self, album, genre_ids, artist_ids)

    def populate(self):
        """
            Populate widget content
        """
        OverlayAlbumHelper.__init__(self)
        self.set_property("halign", Gtk.Align.CENTER)
        self.set_property("valign", Gtk.Align.CENTER)
        self.__widget = Gtk.EventBox()
        grid = Gtk.Grid()
        grid.set_orientation(Gtk.Orientation.VERTICAL)
        self.__label = Gtk.Label()
        self.__label.set_justify(Gtk.Justification.CENTER)
        self.__label.set_ellipsize(Pango.EllipsizeMode.END)
        self.__label.set_property("halign", Gtk.Align.CENTER)
        album_name = GLib.markup_escape_text(self._album.name)
        artist_name = GLib.markup_escape_text(", ".join(self._album.artists))
        self.__label.set_markup("<b>%s</b>\n<span alpha='40000'>%s</span>" %
                                (album_name, artist_name))
        eventbox = Gtk.EventBox()
        eventbox.add(self.__label)
        eventbox.set_property("has-tooltip", True)
        eventbox.connect("query-tooltip", self.__on_query_tooltip)
        eventbox.connect("realize", self._on_realize)
        eventbox.connect("button-press-event",
                         self.__on_artist_button_press)
        eventbox.show()
        self.__widget.add(grid)
        self._overlay = Gtk.Overlay.new()
        self._artwork = App().art_helper.get_image(ArtSize.BIG,
                                                   ArtSize.BIG,
                                                   "cover-frame")
        self._overlay.add(self._artwork)
        grid.add(self._overlay)
        grid.add(eventbox)
        self.add(self.__widget)
        self.set_artwork()
        self.set_selection()
        self.__widget.connect("enter-notify-event", self._on_enter_notify)
        self.__widget.connect("leave-notify-event", self._on_leave_notify)
        self.__widget.connect("button-press-event", self._on_button_press)
        self.connect("destroy", self.__on_destroy)

    def do_get_preferred_width(self):
        """
            Return preferred width
            @return (int, int)
        """
        if self.__widget is None:
            return (0, 0)
        width = Gtk.FlowBoxChild.do_get_preferred_width(self)[0]
        return (width, width)

    @property
    def artwork(self):
        """
            Get album artwork
            @return Gtk.Image
        """
        return self._artwork

    @property
    def is_populated(self):
        """
            True if album populated
        """
        return True

#######################
# PROTECTED           #
#######################
    def _show_overlay_func(self, show_overlay):
        """
            Set overlay
            @param show_overlay as bool
        """
        if self._lock_overlay or\
                self._show_overlay == show_overlay or\
                (App().player.is_locked and show_overlay):
            return
        OverlayAlbumHelper._show_overlay_func(self, show_overlay)
        if show_overlay:
            # Play all button
            self.__play_all_button = Gtk.Button.new()
            self.__play_all_button.set_relief(Gtk.ReliefStyle.NONE)
            self.__play_all_button.set_property("has-tooltip", True)
            self.__play_all_button.set_tooltip_text(_("Play albums"))
            self.__play_all_button.set_property("halign", Gtk.Align.END)
            self.__play_all_button.set_property("valign", Gtk.Align.END)
            self.__play_all_button.connect("realize", self._on_realize)
            self.__play_all_button.connect("clicked",
                                           self.__on_play_all_clicked)
            self.__play_all_button.set_image(Gtk.Image())
            self.__play_all_button.get_image().set_pixel_size(self._pixel_size)
            self.__set_play_all_image()
            self.__play_all_button.show()
            self._overlay_grid.insert_next_to(self._action_button,
                                              Gtk.PositionType.LEFT)
            self._overlay_grid.attach_next_to(self.__play_all_button,
                                              self._action_button,
                                              Gtk.PositionType.LEFT,
                                              1,
                                              1)
            self.__play_all_button.get_style_context().add_class(
                "overlay-button")
        else:
            self.__play_all_button.destroy()
            self.__play_all_button = None

    def _on_album_updated(self, scanner, album_id, destroy):
        """
            On album modified, disable it
            @param scanner as CollectionScanner
            @param album id as int
            @param deleted as bool
            @param destroy as bool
        """
        if self._album.id == album_id and destroy:
            self.destroy()

    def _on_album_artwork(self, surface):
        """
            Set album artwork
            @param surface as str
        """
        if self.__widget is None:
            return
        if surface is None:
            self._artwork.set_from_icon_name("folder-music-symbolic",
                                             Gtk.IconSize.DIALOG)
        else:
            self._artwork.set_from_surface(surface)
        self.show_all()
        self.emit("populated")

#######################
# PRIVATE             #
#######################
    def __set_play_all_image(self):
        """
            Set play all image based on current shuffle status
        """
        if App().settings.get_enum("shuffle") == Shuffle.NONE:
            self.__play_all_button.get_image().set_from_icon_name(
                "media-playlist-consecutive-symbolic",
                Gtk.IconSize.INVALID)
        else:
            self.__play_all_button.get_image().set_from_icon_name(
                "media-playlist-shuffle-symbolic",
                Gtk.IconSize.INVALID)

    def __on_play_all_clicked(self, button):
        """
            Play album with context
            @param button as Gtk.Button
        """
        if App().player.is_locked:
            return True
        self._show_append(False)
        if App().player.is_party:
            App().lookup_action("party").change_state(GLib.Variant("b", False))
        App().player.play_albums(self._album.id,
                                 self._genre_ids,
                                 self._artist_ids)
        return True

    def __on_query_tooltip(self, eventbox, x, y, keyboard, tooltip):
        """
            Show tooltip if needed
            @param eventbox as Gtk.EventBox
            @param x as int
            @param y as int
            @param keyboard as bool
            @param tooltip as Gtk.Tooltip
        """
        layout = self.__label.get_layout()
        if layout.is_ellipsized():
            markup = self.__label.get_label()
            tooltip.set_markup(markup)
            return True

    def __on_artist_button_press(self, eventbox, event):
        """
            Go to artist page
            @param eventbox as Gtk.EventBox
            @param event as Gdk.EventButton
        """
        App().window.container.show_artists_albums(self._album.artist_ids)
        return True

    def __on_destroy(self, widget):
        """
            Destroyed widget
            @param widget as Gtk.Widget
        """
        self.__widget = None
