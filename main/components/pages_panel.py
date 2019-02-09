from sublime_db.core.typecheck import (
	Callable,
	Any,
	List,
	Sequence,
	Tuple
)

from sublime_db import ui
from .constants import VARIABLE_PANEL_MIN_WIDTH


class TabbedPanel(ui.Block):
	def __init__(self, items: List[Tuple[str, ui.Block]], selected_index: int) -> None:
		super().__init__()
		self.items = items
		self.selected_index = selected_index
		self._modified = [] #type: List[bool]
		for item in items:
			self._modified.append(False)

	def selected(self, index: int):
		self.selected_index = index
		self._modified[index] = False
		self.dirty()

	def modified(self, index: int):
		if not self._modified[index] and self.selected_index != index:
			self._modified[index] = True
		self.dirty()

	def render(self) -> ui.Block.Children:
		assert self.layout
		tabs = [] #type: List[ui.Inline]
		for index, item in enumerate(self.items):
			def on_click(index: int = index):
				self.selected(index)
			tabs.append(ui.Button(on_click, items=[
				PageTab(item[0], index == self.selected_index, self._modified[index])
			]))
			tabs.append(ui.HorizontalSpacer(0.25)) #type: ignore
		return [
			ui.block(*tabs),
			ui.HorizontalSpacer(self.layout.width() - VARIABLE_PANEL_MIN_WIDTH - 6.75),
			ui.Panel(items=[
				self.items[self.selected_index][1]
			]),
		]


class PageTab (ui.Inline):
	def __init__(self, name: str, selected: bool, modified: bool) -> None:
		super().__init__()
		if selected:
			self.add_class('selected')
			self.items = [
				ui.Label(name, width=15, align=0),
				ui.Button(self.on_more, items=[
					ui.Img(ui.Images.shared.more)
				])
			]
		elif modified:
			self.items = [
				ui.Label(name, width=15, align=0, color="secondary"),
				ui.Label('◯', width=ui.WIDTH, align=0, color="secondary")
			]
		else:
			self.items = [
				ui.Label(name, width=15 + ui.WIDTH, align=0, color="secondary"),
			]

	def on_more(self) -> None:
		pass

	def render(self) -> ui.Inline.Children:
		return self.items