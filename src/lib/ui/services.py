import PyQt6.QtCore as pyqt6_qtcore
import PyQt6.QtWidgets as pyqt6_qtwidgets
import pydantic
from pydantic import ValidationError

import lib.app.split_settings.ui as app_split_settings_ui
import lib.methods.config as methods_config
import lib.ui.repositories as ui_repositories
import matplotlib.backends.backend_qtagg as matplotlib_backend_qtagg


class UiService(pyqt6_qtwidgets.QMainWindow, ui_repositories.Ui_MainWindow):
    def __init__(self, settings: app_split_settings_ui.UISettings, parent=None):
        super().__init__(parent)
        self.settings = settings
        self.setupUi(self)
        self.list_input.setSpacing(5)
        self.pb_calculate.clicked.connect(self.on_calculate)
        self.method_selected_model, self.method_selected = None, None
        self.text_entry.setText("Здесь будет результат работы программы")
        self.cb_labs.addItems((f"Лабораторная работа №{i}" for i in range(2, self.settings.labs_count + 2)))
        self.cb_labs.activated.connect(self.on_lab)
        self.lab_number = 1
        self.variant_number = 1
        self.methods = methods_config.LAB_1_METHODS
        self.connect_list_widget()
        self.method_title: str | None = None
        self.input_data: pydantic.BaseModel | None = None
        self.input_data_method: str | None = None
        self.list_widget = None

    def on_lab(self, value):
        self.lab_number = value + 1
        if self.lab_number == 1:
            self.methods = methods_config.LAB_1_METHODS

        self.set_methods()

    def create_fields_input(
            self, titles: list[str], values_names: list[str], values_default: list[methods_config.FIELD_DEFAULT_TYPE]
    ):
        self.list_input.clear()
        for i in range(len(titles)):
            self.create_field_input(i, titles[i], values_names[i], values_default[i])

    def create_field_input(
            self,
            field_number: int,
            title: str,
            value_name: str,
            value_default: methods_config.FIELD_DEFAULT_TYPE = None,
    ):
        item = pyqt6_qtwidgets.QListWidgetItem()
        item.setTextAlignment(pyqt6_qtcore.Qt.AlignmentFlag.AlignHCenter)
        self.list_input.addItem(item)
        widget = ui_repositories.CustomWidget(field_number, title, value_name, value_default)
        self.list_input.setItemWidget(item, widget)

    def set_methods(self):
        self.list_methods.clear()
        self.list_methods.addItems(list(self.methods.keys()))
        self.text_entry.setText("Здесь будет результат работы программы")

    def connect_list_widget(self) -> None:
        self.set_methods()
        self.list_methods.itemDoubleClicked.connect(self.select_method)

    def select_method(self, item: pyqt6_qtwidgets.QListWidgetItem) -> None:
        self.text_entry.setText("Здесь будет результат работы программы")

        self.method_title = item.text()
        assert self.method_title in self.methods

        self.method_selected_model, self.method_selected = self.methods[self.method_title]
        model_schema = self.method_selected_model.model_json_schema()
        if "required" in model_schema:
            model_schema.pop("required")
        titles = [
            value["description"]
            for value in model_schema["properties"].values()
            if value["description"] != "Not expected"
        ]
        values_names = list(model_schema["properties"].keys())
        values_default = [value.get("default") for value in model_schema["properties"].values()]
        if self.input_data and self.input_data_method == self.method_title:
            values_default = list(self.input_data.model_dump().values())
        self.create_fields_input(titles, values_names, values_default)
        if self.list_widget:
            self.layout_output_pictures.removeWidget(self.list_widget)
            self.list_widget.deleteLater()
            self.list_widget = None

    def get_input_text(self) -> pydantic.BaseModel:
        if not self.method_selected_model:
            raise ValueError
        items = [self.list_input.item(row) for row in range(self.list_input.count())]
        input_values = {
            self.list_input.itemWidget(item).text()[0]: self.list_input.itemWidget(item).text()[1].replace(",", ".")
            # type: ignore
            for item in items
        }
        input_values["variant"] = self.variant_number
        try:
            values_validated = self.method_selected_model.model_validate(input_values)
        except AttributeError:
            raise ValueError("Ошибка: Ни одного параметра не введено")
        return values_validated

    @classmethod
    def __get_error_message(cls, errors: list):
        error_messages = []
        for error in errors:
            message = error.get("msg")
            message = f"Ошибка валидации типа {message.split()[-1]}" if message.startswith("value is not") else message
            error_messages.append(f"{message}. Поле: {', '.join(error.get('loc'))}")
        return "\n".join(error_messages)

    def on_save_input(self):
        if not self.method_selected:
            self.text_entry.setText("Сначала нужно выбрать метод")
            return
        self.input_data = self.get_input_text()
        self.input_data_method = self.method_title
        self.text_entry.setText("Данные успешно сохранены")

    def on_calculate(self):
        if not self.method_selected:
            self.text_entry.setText("Сначала нужно выбрать метод")
            return
        if self.list_widget:
            self.layout_output_pictures.removeWidget(self.list_widget)
            self.list_widget.deleteLater()
        try:
            input_data = self.get_input_text()
            result = self.method_selected(input_data)
            if isinstance(result, tuple):
                result, graphs = result
                self.graphs = graphs

                self.list_widget = pyqt6_qtwidgets.QListWidget()
                if self.method_title == "Первая часть":
                    graphs_names = list(methods_config.LAB_1_GRAPHS_1.keys())
                else:
                    graphs_names = list(methods_config.LAB_1_GRAPHS_2.keys())

                list_widget_item = pyqt6_qtwidgets.QListWidgetItem(graphs_names[0])
                list_widget_item2 = pyqt6_qtwidgets.QListWidgetItem(graphs_names[1])
                list_widget_item3 = pyqt6_qtwidgets.QListWidgetItem(graphs_names[2])
                list_widget_item4 = pyqt6_qtwidgets.QListWidgetItem(graphs_names[3])
                list_widget_item5 = pyqt6_qtwidgets.QListWidgetItem(graphs_names[4])

                self.list_widget.addItem(list_widget_item)
                self.list_widget.addItem(list_widget_item2)
                self.list_widget.addItem(list_widget_item3)
                self.list_widget.addItem(list_widget_item4)
                self.list_widget.addItem(list_widget_item5)

                self.layout_output_pictures.addWidget(self.list_widget)

                self.list_widget.itemDoubleClicked.connect(self.show_graph)

            result = str(result)

        except ValidationError as e:
            result = self.__get_error_message(e.errors())
        # except ValueError as e:
        #     result = str(e)
        # except RecursionError:
        #     result = "Ошибка: Бесконечный цикл. Проверьте значение шага."
        # except ZeroDivisionError:
        #     result = "Ошибка: Деление на ноль. Проверьте введенные значения"
        except Exception as e:
            print(e)
            result = "Ошибка при выполнении программы. Проверьте введенные значения"

        self.text_entry.setText(result)

    def show_graph(self, item: pyqt6_qtwidgets.QListWidgetItem):
        if self.method_title == "Первая часть":
            graphs = methods_config.LAB_1_GRAPHS_1
        else:
            graphs = methods_config.LAB_1_GRAPHS_2
        graph = self.graphs[graphs[item.text()] - 1]
        graph_copy = graph.get_copy()

        ClssDialog(graph_copy, self).exec()


class ClssDialog(pyqt6_qtwidgets.QDialog):
    def __init__(self, graph: matplotlib_backend_qtagg.FigureCanvasQTAgg, parent=None):
        super(ClssDialog, self).__init__(parent)

        self.graph = graph

        self.resize(1700, 1000)
        self.setMinimumSize(pyqt6_qtcore.QSize(1700, 1000))

        self.verticalLayout = pyqt6_qtwidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.layout_output_pictures = pyqt6_qtwidgets.QVBoxLayout()
        self.layout_output_pictures.setObjectName("layout_output_pictures")
        self.verticalLayout.addLayout(self.layout_output_pictures)
        self.layout_output_pictures.addWidget(graph)
        self.setWindowTitle("Dialog")

    def closeEvent(self, event):
        self.close()
        self.graph.deleteLater()
