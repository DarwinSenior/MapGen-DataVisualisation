<app>
	<div class="row">
		<maplist class="col s4" />
		<listview class="col s4" />
	</div>
	<modal mid="addMap">
		<add-file></add-file>
	</modal>
	<modal mid="deleteMap">
		<delete-file></delete-file>
	</modal>
	<modal mid="modifyMap">
		<modify-file></modify-file>
	</modal>
	<script>
	this.on("mount", function(){
		console.log("mounted");
	});
	</script>
</app>