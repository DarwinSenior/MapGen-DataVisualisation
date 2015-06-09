riot.tag('add-file', '<div class="modal-content"> <form action="#" name="xform"> <div class="input-field col s6"> <input id="add_file_name" type="text" class="validate" name="name"> <label for="add_file_name">Name</label> </div> <div class="file-field input-field"> <input disabled value="{fileName}" class="file-path validate" type="text"> <div class="btn"> <span>File</span> <input type="file" name="csv" onchange="{getFileName}"> </div> </div> </form> </div> <div class="modal-footer"> <btn click="{cancel}">Cancel <i class="fa fa-times"></i></btn> <btn click="{okay}">OK <i class="fa fa-check"></i></btn> </div>', function(opts) {
		this.fileName = ""
		this.okay = function(){
			var form_data = new FormData(this.xform)
			console.log(form_data)
			mapActions.addMap(form_data);
			modalActions.closeModal();
		}
		this.cancel = function(){
			modalActions.closeModal();
		}
		this.getFileName = function(){
			this.fileName = this.csv.files[0].name.split('\\').pop();
			this.update();
		}
	
});