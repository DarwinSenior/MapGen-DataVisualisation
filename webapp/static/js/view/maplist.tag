<maplist>
	<ul class="collection with-header">
		<li class="collection-header"><h4>Choose Map</h4></li>
		<listitem each={items} iid={id} name={name} status={status} activated={parent.isActivated(id)}/>
		<li class="collection-item center-align" onclick={addmap}>
			<a href="#">
				<i class="fa fa-plus"></i>
			</a>
		</li>
	</ul>
	<script>
		this.addmap = function(){
			modalActions.openModal("addMap");
		}
		this.updateMaps = function(new_maps, updatemaps, entermaps, exitmaps){
			// var callback = _.after(exitmaps.length+1, (function(){
			// 	this.items = new_maps;
			// 	this.update();
			// }).bind(this));
			// exitmaps.forEach(function(item){
			// 	console.log($(this).find("[iid='"+item.id+"']"))
			// 	$(this[item.name]).hide(callback);
			// });
			// callback();
			this.items = new_maps;
			this.update();
		}
		this.isActivated = function(id){
			return mapActivateStore.isActivated(id);
		}
		this.items = [];
		mapsStore.listen((this.updateMaps).bind(this));
		mapActivateStore.listen((this.update).bind(this));
		mapActions.getMaps();
	</script>
</maplist>