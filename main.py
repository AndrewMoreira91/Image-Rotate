import flet as ft
from PIL import Image
import time

def main(page: ft.Page):
    page.title = "Image Rotate"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.bgcolor = "#f0f0f0"
    page.window_resizable = True
    page.window_width = 800
    page.window_height = 650
    page.window_min_width = 600
    page.window_min_height = 600

    files = []
    
    text_select_images_count = ft.Text(
        "Nenhuma imagem selecionada",
        size=24,
        color=ft.colors.GREY_500,
        weight=ft.FontWeight.BOLD,
    )
    
    text_rotated_images_count = ft.Text(
        "0 imagens rotacionadas",
        size=16,
        color=ft.colors.GREY_600,
        visible=False
    )
    
    progress_bar = ft.ProgressBar(
        width=500, bgcolor=None, color=ft.colors.CYAN_500, visible=True
    )
    
    conteiner_pb = ft.Column([
        ft.Text("Rotacionando imagens...", size=16, color=ft.colors.BLACK),
        progress_bar,
    ],
        alignment=ft.MainAxisAlignment.CENTER,
        visible=False,
        height=50
    )
    
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

    def rotate_images(degrees: int):
        images_rotated_count = 0
        print(f"Rotating images {degrees} degrees")
        if len(files) == 0:
            return
        incremento = (100 / len(files)) / 100
        progresso = 0
        while len(files) > 0:
            progresso = progresso + incremento
            # print(progresso)
            file = files.pop(0)
            progress_bar.value = progresso
            conteiner_pb.visible = True
            text_rotated_images_count.visible = True
            text_select_images_count.visible = False
            page.update()
            try:
                img = Image.open(file.path)
                # print(f"Image {file.name} opened")
                width, height = img.size
                if width < height:
                    img.rotate(degrees, expand=True).save(file.path)
                    print(f"Image {file.name} rotated {degrees} degrees")
                    images_rotated_count += 1
                text_rotated_images_count.value = f"{len(files)} imagens restantes - {images_rotated_count} imagens rotacionadas"
                page.update()
            except Exception as e:
                print(f"An error occurred: {e}")
            time.sleep(0.1)

        conteiner_pb.visible = False
        progress_bar.value = 0
        text_rotated_images_count.visible = False

        if images_rotated_count == 0:
            return "Nenhuma imagem rotacionada!"
        else:
            return str(images_rotated_count) + " imagens rotacionadas com sucesso!"

    def handle_click(e):
        response = rotate_images(90)
        open_dialog_modal(response)
        files.clear()

    def update_text_number_files():
        text_select_images_count.visible = True
        if len(files) == 0:
            text_select_images_count.value = "Nenhuma imagem selecionada"
            buttonRotate.disabled = True
        elif len(files) >= 1:
            text_select_images_count.value = f"{len(files)} imagens selecionadas"
            buttonRotate.disabled = False
        page.update()

    def open_dialog_modal(content: str):
        dlg_modal.content = ft.Text(content)
        page.dialog = dlg_modal
        dlg_modal.open = True
        page.update()

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
                                allow_multiple=True,
                                allowed_extensions=["png", "JPEG"]
                            ),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    height=70,
                ),
                ft.Row(
                    [
                        text_select_images_count,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [
                        buttonRotate,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [
                        conteiner_pb,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [
                        text_rotated_images_count,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            spacing=0,
        )
    )


ft.app(target=main)
