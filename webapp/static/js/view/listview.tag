<listview>
	<div name="wrapper">
		<div each={items} class="card-panel">
			<div class="center-align">
				{name}
			</div>
			<div class="section"/>
			<mapview iid={id} syncmaps={parent.syncmaps}></mapview>
		</div>
	</div>
	<script>
		this.items = mapActivateStore.activateMapList();
		this.updateList = function(){
			this.items = mapActivateStore.activateMapList();
			this.update();
			$(this.collapsible).collapsible();
		}
		this.syncmaps = {};
		// Sortable.create(this.wrapper);
		mapActivateStore.listen((this.updateList).bind(this));
	</script>
</listview>