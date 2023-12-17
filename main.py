from PIL import Image
Image.CUBIC = Image.BICUBIC
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.toast import ToastNotification
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.validation import add_regex_validation

# Frame = container
class Gradebook(tb.Frame):
    def __init__(self, master_window):
        super().__init__(master_window, padding=(20, 10))
        self.pack(fill=BOTH, expand=YES)
        self.name = tb.StringVar(value="")
        self.student_id = tb.StringVar(value="")
        self.course_name = tb.StringVar(value="")
        self.final_score = tb.DoubleVar(value=0)
        self.data = []
        self.colors = master_window.style.colors

        instruction_text = "Please enter your contact information: "
        instruction = tb.Label(self, text = instruction_text, width = 50)
        instruction.pack(fill = X, pady = 10)

        self.create_form_entry("Name: ", self.name)
        self.create_form_entry("Student ID: ", self.student_id)
        self.create_form_entry("Course Name: ", self.course_name)
        self.final_score_input = self.create_form_entry("Final Score: ", self.final_score)

        self.create_meter()
        self.create_buttonbox()

        self.table = self.create_table()

    # Create text/numerical inputs
    def create_form_entry(self, label, variable):
        form_field_container = tb.Frame(self)
        form_field_container.pack(fill=X, expand=YES, pady=5)

        form_field_label = tb.Label(master=form_field_container, text = label, width = 50)
        form_field_label.pack(side = LEFT, padx = 12)

        form_input = tb.Entry(master=form_field_container, textvariable=variable)
        form_input.pack(side = LEFT, padx = 5, fill= X, expand=YES)

        add_regex_validation(form_input, r'^[a-zA-Z0-9_]*$')
        
        return form_input
    
    # Create meter
    def create_meter(self):
        meter = tb.Meter(
            master = self,
            metersize = 150,
            padding = 5,
            amounttotal = 100,
            amountused = 50,
            metertype= "full",
            subtext = "Final Score",
            interactive = True
        )

        meter.pack()
        self.final_score.set(meter.amountusedvar)
        self.final_score_input.configure(textvariable = meter.amountusedvar)
    
    # Create buttons
    def create_buttonbox(self):
        button_container = tb.Frame(self)
        button_container.pack(fill=X, expand=YES, pady=(15, 10))

        cancel_button = tb.Button(
            master = button_container,
            text = "Cancel",
            command = self.on_cancel,
            bootstyle=DANGER,
            width = 6
        )
        cancel_button.pack(side=RIGHT, padx=5)

        submit_button = tb.Button(
            master = button_container,
            text = "Submit",
            command = self.on_submit,
            bootstyle=SUCCESS,
            width = 6
        )
        submit_button.pack(side=RIGHT, padx=5)
    
    def on_submit(self):
        name = self.name.get()
        student_id = self.student_id.get()
        course_name = self.course_name.get()
        final_score = self.final_score_input.get()
        
        toast = ToastNotification(
            title="Success",
            message="Submitted",
            duration=3000
        )
        toast.show_toast()

        self.data.append((name, student_id, course_name, final_score))
        self.table.destroy()
        self.table = self.create_table()
    
    def on_cancel(self):
        self.quit()
    
    def create_table(self):
        coldata = [
            {"text": "Name"},
            {"text": "Student ID", "stretch": False},
            {"text": "Course Name"},
            {"text": "Final Score", "stretch": False},
        ]

        table = Tableview(
            master=self,
            coldata=coldata,
            rowdata=self.data,
            paginated=True,
            searchable=True,
            bootstyle=PRIMARY,
            stripecolor=(self.colors.light, None)
        )

        table.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        return table

if __name__ == "__main__":
    app = tb.Window("Gradebook", "superhero", resizable=(False, False))
    Gradebook(app)
    app.mainloop()
