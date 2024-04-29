import flet as ft
import cv2
import numpy as np

def main(page: ft.Page):
    page.title = "Image Rotate"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.bgcolor = "#f0f0f0"
    page.window_resizable = True
    page.window_width = 800
    page.window_height = 650

    files = []

    def rotate_images(degrees: int):
        number_files_rotate = 0
        print(f"Rotating images {degrees} degrees")
        if len(files) == 0:
            return
        for file in files:
            try:
                img = cv2.imread(file.path)
                height, width = img.shape[:2]
                if width < height:
                    center = (width / 2, height / 2)
                    rotation_matrix = cv2.getRotationMatrix2D(center, -90, 1.0)
                    cos = np.abs(rotation_matrix[0, 0])
                    sin = np.abs(rotation_matrix[0, 1])
                    new_width = int((height * sin) + (width * cos))
                    new_height = int((height * cos) + (width * sin))

                    rotation_matrix[0, 2] += (new_width / 2) - center[0]
                    rotation_matrix[1, 2] += (new_height / 2) - center[1]
                    rotated_image = cv2.warpAffine(img, rotation_matrix, (new_width, new_height), flags=cv2.INTER_LINEAR)
                    cv2.imwrite(file.path, rotated_image)
                    print(f"Image {file.name} rotated {degrees} degrees")
                    number_files_rotate += 1
            except Exception as e:
                print(f"An error occurred: {e}")
        if number_files_rotate == 0:
            return "Nenhuma imagem rotacionada!"
        else:
            return str(number_files_rotate) + " imagens rotacionadas com sucesso!"

    def handle_click(e):
        response = rotate_images(90)
        open_dialog_modal(response)
        files.clear()

    def update_text_number_files():
        if len(files) == 0:
            textNumberFiles.value = "Nenhuma imagem selecionada"
            buttonRotate.disabled = True
        elif len(files) >= 1:
            textNumberFiles.value = f"{len(files)} imagens selecionadas"
            buttonRotate.disabled = False
        page.update()

    def open_dialog_modal(content: str):
        dlg_modal.content = ft.Text(content)
        page.dialog = dlg_modal
        dlg_modal.open = True
        page.update()

    def close_dlg(e):
        dlg_modal.open = False
        update_text_number_files()
        page.update()

    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Imagens Rotacionadas com Sucesso!"),
        actions=[
            ft.TextButton("Ok", on_click=close_dlg),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=lambda e: print("Modal dialog dismissed!"),
    )

    def pick_files_result(e: ft.FilePickerResultEvent):
        if e.files is None:
            print("No files selected")
            files.clear()
            update_text_number_files()
            return
        print(f"Selected {len(e.files)} files")
        for file in e.files:
            files.append(file)
        update_text_number_files()

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    page.overlay.append(pick_files_dialog)

    textNumberFiles = ft.Text(
        "Nenhuma imagem selecionada",
        size=24,
        color=ft.colors.GREY_500,
        weight=ft.FontWeight.BOLD,
    )
    buttonRotate = ft.OutlinedButton(
        "Rotacionar Imagens",
        width=500,
        height=50,
        disabled=True,
        on_click=handle_click,
    )

    page.add(
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Image(
                            src="assets/icon.png",
                            rotate=0,
                            scale=1,
                            height=160,
                            width=160,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [
                        ft.Text(
                            "Selecione as imagens",
                            size=36,
                            color=ft.colors.CYAN_500,
                            weight=ft.FontWeight.BOLD,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    height=70,
                ),
                ft.Row(
                    [
                        ft.ElevatedButton(
                            "Selecionar Imagens",
                            bgcolor=ft.colors.CYAN_300,
                            color=ft.colors.WHITE,
                            width=500,
                            height=50,
                            on_click=lambda _: pick_files_dialog.pick_files(
                                allow_multiple=True
                            ),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    height=70,
                ),
                ft.Row(
                    [
                        textNumberFiles,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [
                        buttonRotate,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            spacing=0,
        )
    )


ft.app(target=main)
