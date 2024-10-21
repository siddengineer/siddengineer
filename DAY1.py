import flet as ft

def main(page: ft.Page):
    tasks = []

    def add_task(e):
        if task_input.value:
            task_control = ft.Row(
                controls=[
                    ft.Text(task_input.value, width=200),
                    ft.IconButton(
                        icon=ft.icons.CHECK,
                        on_click=lambda e, task=task_input.value: mark_completed(task)
                    ),
                    ft.IconButton(
                        icon=ft.icons.DELETE,
                        on_click=lambda e, task=task_input.value: delete_task(task)
                    ),
                ]
            )
            tasks.append(task_input.value)
            tasks_list.controls.append(task_control)
            task_input.value = ""
            page.update()

    def delete_task(task):
        for control in tasks_list.controls:
            if control.controls[0].value == task:
                tasks_list.controls.remove(control)
                tasks.remove(task)
                page.update()
                break

    def mark_completed(task):
        for control in tasks_list.controls:
            if control.controls[0].value == task:
                # Update the task to show it's completed
                control.controls[0].value = f"[Completed] {task}"
                control.controls[0].style = "text-decoration: line-through;"
                page.update()
                break

    task_input = ft.TextField(hint_text="Write a new task", width=300)
    add_task_button = ft.ElevatedButton(text="Add task", on_click=add_task)
    tasks_list = ft.Column()

    # Add input field, button, and task list to the page
    page.add(
        ft.Text("Today's My Tasks", size=24, weight="bold"),  # Heading
        task_input,
        add_task_button,
        tasks_list
    )
    page.update()

ft.app(target=main)
