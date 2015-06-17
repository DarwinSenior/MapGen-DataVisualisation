<modify-file>
	<div class="modal-content">
		<div class="progress" if={!loaded}>
      		<div class="indeterminate"></div>
  		</div>
		<div class="input-field" if={loaded}>
			<div class="row">
				<label>Choose the color</label>
			</div>
			<div class="row">
			<div class="col s3" each={csvhead}>
				<input name="group1" type="radio" id={item+'selector'} value={item} onchange={(parent.select).bind(parent)} checked={parent.color == item}/>
	    		<label for={item+'selector'}>{item}</label>
	    	</div>
	    	</div>
		</div>
	</div>
	<div class="modal-footer">
		<btn click={cancel}>Cancel <i class="fa fa-times"></i></btn>
		<btn click={okay}>OK <i class="fa fa-check"></i></btn>
	</div>
	<script>
		this.loaded = false;
		this.getArgs = function(){
			var args = this.parent.args;
			if (this.id != args.id){
				this.id = args.id;
				this.name = args.name;
				this.csvhead = [];
				this.loaded = false;
				mapItemActions.getItem(this.id);	
			}
		}
		this.select = function(evt){
			console.log(this.color);
			this.color = evt.target.value;
		}
		this.getCSVHead = function(data){
			this.loaded = true;
			this.csvhead = data.header.map(function(item){return {item: item}});
			this.color = data.color;
			this.update();
		}
		this.okay = function(){
			mapItemActions.postItem(this.id, {'color' : this.color});
			mapActivateActions.deactivateMap(this.id);
			this.cancel();
		}
		this.cancel = function(){
			this.name = undefined;
			this.id = undefined;
			modalActions.closeModal();
		}
		this.on("update", (this.getArgs).bind(this));
		mapItemStore.listen((this.getCSVHead).bind(this));

	</script>
</modify-file>