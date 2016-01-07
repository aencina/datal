var theme6View = Backbone.Epoxy.View.extend({
	el: '#id_themeForm',
	template: null,
	sliderFiles: [],
	buttonFiles: [],
	sliderInputCont: 0,
	buttonsCont: 0,
	middleBottomImage : "",
	leftBottomImage : "",
	rightBottomImage : "",

	events: {
		"click #id_new_slide": "addSliderInput",
		"click #id_new_button": "addButtonsInput",
		"click #id_btnRemoveLeftBottom" : "removeLeftBottomImage",
		"click #id_btnRemoveMiddleBottom" : "removeMiddleBottomImage",
		"click #id_btnRemoveRightBottom" : "removeRightBottomImage",
		"change #id_radios input[type='radio']": "onRadioChange"
	},

	initialize: function(options) {
		this.currentView = options.currentView;
        this.currentModel = options.currentModel;

		this.currentView.helpAndTips('hide');
		that = this;
		this.template = _.template($("#id_theme6Template").html());
		this.render();
		this.initSliderSection();
		this.initButtonSection();
		this.initMiddleBottomImage();
		this.initLeftBottomImage();
		this.initRightBottomImage();
	},

	render: function() {
		this.$el.html(this.template(this.model.attributes));
		return this;
	},
	createAddTemplateImageInputRow: function(intId, inputId, section) {
		var linkText = gettext('ADMIN-HOME-SECTION-LINKTEXT');
		var deleteText = gettext('ADMIN-HOME-SECTION-DELETESLIDE');
		var descriptionLabelText = gettext('APP-DESCRIPTION2-LABEL');
		var videoLabelText = gettext('ADMIN-HOME-SECTION-VIDEOTEXT');
		var descriptionPlaceHolderText = gettext('APP-DESCRIPTION2-TEXT');
		var placeholderText = gettext('ADMIN-HOME-SECTION-LINKPLACEHOLDER');
		var videoPlaceholderText = gettext('ADMIN-HOME-SECTION-VIDEOPLACEHOLDER');
		var buttonText = gettext('ADMIN-HOME-SECTION-BUTTONTEXT');
		var html = 
			'<tr class=\"template-upload fade\" id=\"row' + intId + '\">' +
				'<td>' +
					'<div class=\"clearfix\">' +

						'<div class=\"FL clearfix\">' +
							'<div class=\"crop relative clearfix FL\">' +
								'<button class=\"button small\">' + buttonText + '</button>' +
								'<input type=\"file\" id=\"' + inputId + '\" class=\"file FL\" tabindex=\"-1\"/>' +
							'</div>' +
						'</div>' +

						'<div class=\"FR\">' +
							'<input type=\"button\" id=\"del_' + section + intId + '\" class=\"remove FL\" value=\"' + deleteText + '\"/>' +
						'</div>' +
						
						'<div class=\"FR sliderData\">' +

							'<div class=\"clearfix rowSeparation\">' +
								'<label for=\"description_' + section + intId + '\" class=\"FL\">' + descriptionLabelText + '</label>' +
								'<div class=\"formErrorMessageContainer FL\">' +
									'<input type=\"text\" id=\"description_' + section + intId + '\" name=\"description_' + section + intId + '\" class=\"field FL requiredText\" placeholder=\"' + descriptionPlaceHolderText + '\"/>' +
								'</div>' +
							'</div>' +

							'<div id=\"id_radios\">' +
								'<label></label>' +
								'<input class=\"linkRadio\" type=\"radio\" value=\"linkSection\" id=\"id_radios_link_' + section + intId + '\" name=\"radios_' + section + intId + '\" checked=\"checked\"/>' +
								'<label for=\"id_radios_link_' + section + intId + '\" class=\"radioLabel linkLabel\">' + linkText + '</label>' +
								'<input class=\"videoRadio\" type=\"radio\" value=\"videoSection\" id=\"id_radios_video_' + section + intId + '\" name=\"radios_' + section + intId + '\"/>' +
								'<label for=\"id_radios_video_' + section + intId + '\" class=\"radioLabel videoLabel\">' + videoLabelText + '</label>' +
							'</div>' +

							'<div class=\"clearfix linkSection radioSection\">' +
								'<label for=\"link_' + intId + '\"class=\"FL\"></label>' +
								'<div class=\"formErrorMessageContainer FL\">' +
									'<input type=\"url\" id=\"link_' + section + intId + '\" class=\"field FL urlLink complete_url\" placeholder=\"' + placeholderText + '\"/>' +
								'</div>' +
							'</div>' +

							'<div class=\"clearfix videoSection radioSection\" style=\"display:none;\">' +
								'<label for=\"video_' + intId + '\"class=\"FL\"></label>' +
								'<div class=\"formErrorMessageContainer FL\">' +
									'<textarea id=\"video_' + section + intId + '\" rows="" cols="" class=\"field FL video_url\" placeholder=\"' + videoPlaceholderText + '\"></textarea>' +
								'</div>' +
							'</div>' +

						'</div>' +

					'</div>' +
				'</td>' +
			'</tr>';
		return html;
	},
	createSavedTemplateImageInputRow: function(rowIndex, item, inputId, section) {
		var linkText = gettext('ADMIN-HOME-SECTION-LINKTEXT');
		var deleteText = gettext('ADMIN-HOME-SECTION-DELETESLIDE');
		var descriptionLabelText = gettext('APP-DESCRIPTION2-LABEL');
		var videoLabelText = gettext('ADMIN-HOME-SECTION-VIDEOTEXT');
		var descriptionPlaceHolderText = gettext('APP-DESCRIPTION2-TEXT');
		var placeholderText = gettext('ADMIN-HOME-SECTION-LINKPLACEHOLDER');
		var videoPlaceholderText = gettext('ADMIN-HOME-SECTION-VIDEOPLACEHOLDER');
		var buttonText = gettext('ADMIN-HOME-SECTION-BUTTONTEXT');

		var linkChecked = "";
		var videoChecked = "";
		var linkContainer = "none";
		var videoContainer = "none";

		if(item.radio == "videoSection"){
			videoChecked = 'checked=\"checked\"';
			videoContainer = "block";
		}
		if(item.radio == "linkSection"){
			linkChecked = 'checked=\"checked\"';
			linkContainer = "block";
		}

		var html = 
			'<tr class=\"template-upload fade\" id=\"row' + rowIndex + '\">' +
				'<td class=\"draggableSection\"><i class=\"arrangeIcon\"></i></td>' +
				'<td>' +
					'<div class=\"clearfix\">' +

						'<div class=\"FL clearfix\">' +
							'<img src=\"' + item.image + '\" alt=\"\" class=\"FL\"/>' +
							'<div class=\"crop relative clearfix FL\">' +
								'<button class=\"button small\">' + buttonText + '</button>' +
								'<input type=\"file\" id=\"' + inputId + '\" class=\"file FL\" tabindex=\"-1\"/>' +
							'</div>' +
						'</div>' +

						'<div class=\"FR\">' +
							'<input type=\"button\" id=\"del_' + section + rowIndex + '\" class=\"remove FL\" value=\"' + deleteText + '\"/>' +
						'</div>' +

						'<div class=\"FR sliderData\">' +

							'<div class=\"clearfix rowSeparation\">' +
								'<label for=\"description_' + section + rowIndex + '\" class=\"FL\">' + descriptionLabelText + '</label>' +
								'<div class=\"formErrorMessageContainer FL\">' +
									'<input type=\"text\" id=\"description_' + section + rowIndex + '\" value=\"' + item.description + '\" name=\"description_' + section + rowIndex + '\" class=\"field FL requiredText\" placeholder=\"' + descriptionPlaceHolderText + '\"/>' +
								'</div>' +
							'</div>' +

							'<div id=\"id_radios\">' +
								'<label></label>' +
								'<input class=\"linkRadio\" type=\"radio\" value=\"linkSection\" id=\"id_radios_link_' + section + rowIndex + '\" name=\"radios_' + section + rowIndex + '\"' + linkChecked +'/>' +
								'<label for=\"id_radios_link_' + section + rowIndex + '\" class=\"radioLabel linkLabel\">' + linkText + '</label>' +
								'<input class=\"videoRadio\" type=\"radio\" value=\"videoSection\" id=\"id_radios_video_' + section + rowIndex + '\" name=\"radios_' + section + rowIndex + '\"' + videoChecked + '/>' +
								'<label for=\"id_radios_video_' + section + rowIndex + '\" class=\"radioLabel videoLabel\">' + videoLabelText + '</label>' +
							'</div>' +

							'<div class=\"clearfix linkSection radioSection\" style=\"display:' + linkContainer + '\">' +
								'<label for=\"link_' + section + rowIndex + '\" class=\"FL\"></label>' +
								'<div class=\"formErrorMessageContainer FL\">' +
									'<input type=\"url\" id=\"link_' + section + rowIndex + '\" value=\"' + item.href + '\" class=\"field FL urlLink complete_url\" placeholder=\"' + placeholderText + '\"/>' +
								'</div>' +
							'</div>' +

							'<div class=\"clearfix videoSection radioSection\" style=\"display:' + videoContainer + '\">' +
								'<label for=\"video_' + section + rowIndex + '\" class=\"FL\"></label>' +
								'<div class=\"formErrorMessageContainer FL\">' +
									'<textarea id=\"video_' + section + rowIndex + '\" rows="" cols="" class=\"field FL video_url\" placeholder=\"' + videoPlaceholderText + '\">'+ item.video +'</textarea>' +
								'</div>' +
							'</div>' +

						'</div>' +

					'</div>' +
				'</td>' +
			'</tr>';
		return html;
	},

	/*
	 * This function will initialize the images input based on the saved
	 * preference
	 */
	initSliderSection: function() {
		var that = this;
		_.each(this.model.get('imageSliderSection'), function(item, index) {
			console.log(item);
			var intId = that.sliderInputCont;
			var inputId = "file_image" + intId;
			var row = that.createSavedTemplateImageInputRow(intId, item, inputId, "slider");

			$("#image_table").append(row);

			// Add spacebar, enter and click to browse button, to trigger file upload
			that.setBrowseButtonTrigger(intId);

			$("#link_slider" + intId).on('change', function() {
				var image = that.model.get('imageSliderSection')[index];
				image.href = $("#link_slider" + intId).val();
				that.model.get('imageSliderSection').splice(index, 1, image);
				image = null;
			});

			$("#description_slider" + intId).on('change', function() {
					var image = that.model.get('imageSliderSection')[index];
					image.description = $("#description_slider" + intId).val();
					that.model.get('imageSliderSection').splice(index, 1, image);
					image = null;
			});

			$("#video_slider" + intId).on('change', function() {
					var image = that.model.get('imageSliderSection')[index];
					image.video = $("#video_slider" + intId).val();
					that.model.get('imageSliderSection').splice(index, 1, image);
					image = null;
			});

			// We make the table sortable
			that.setTableSortable($('#image_table'), that.model.get('imageSliderSection'));


			// When clicked delete button the object is removed from the model

			$("#del_slider" + intId).on('click', function() {
				that.model.attributes.imageSliderSection.splice($('#' + inputId).closest('tr').index(), 1)
				$.each(that.sliderFiles, function(index, item) {
					if (item.input[0].id.indexOf('#' + inputId) >= 0) {
						that.sliderFiles.splice(index, 1)
						return false;
					}
				});

				$(this).closest("tr").remove();

			});
			that.setUploadable($('#' + inputId), "slider");
			that.sliderInputCont += 1;
		});

	},


	/*
	 * This function is called when we want to add a new image input. The files
	 * already saved will be stored in image_table, whilst those input that are
	 * created when clicking "add new slide" will be added to image_saved table.
	 * This is done to reduce code complexity when sorting the inputs.
	 */
	addSliderInput: function() {
		if ($("#image_saved tr").length < 1) {
			var that = this;
			var intId = that.sliderInputCont;
			var inputId = "file_image" + intId;
			that.sliderInputCont += 1;
			var row = that.createAddTemplateImageInputRow(intId, inputId, "slider");

			$("#image_saved").append(row);

			// Add spacebar, enter and click to browse button, to trigger file upload
			this.setBrowseButtonTrigger(intId);

			$("#del_slider" + intId).on('click', function() {
				var table = $("#del_slider" + intId).closest("table");
				if (table.is("#image_table")) {
					if (($("#image_table tr").length) == that.model.attributes.imageSliderSection.length) {
						that.model.attributes.imageSliderSection.splice($('#' + inputId).closest('tr').index(), 1);
					}
					$.each(that.sliderFiles, function(index, item) {
						if (item.input[0].id.indexOf('#' + inputId) >= 0) {
							that.sliderFiles.splice(index, 1)
							return false;
						}
					});
				}
				$(this).closest("tr").remove();
			});

			$("#link_slider" + intId).on('change', function() {
				var index = $("#link_slider" + intId).closest('tr').index();
				if (that.model.attributes.imageSliderSection.length > index && that.model.attributes.imageSliderSection[index] != undefined) {
					var image = that.model.get('imageSliderSection')[index];
					image.href = $("#link_slider" + intId).val();
					that.model.get('imageSliderSection').splice(index, 1, image);
				}
			});

			$("#description_slider" + intId).on('change', function() {
				var index = $("#description_slider" + intId).closest('tr').index();
				if (that.model.attributes.imageSliderSection.length > index && that.model.attributes.imageSliderSection[index] != undefined) {
						var image = that.model.get('imageSliderSection')[index];
						image.description = $("#description_slider" + intId).val();
						that.model.get('imageSliderSection').splice(index, 1, image);
				}
			});

			// $("#id_radios input[name='radios_slider" + intId + "']").on('change', function() {
			// 	console.log("Radio");
			// 	var index = $("#id_radios input[name='radios_slider" + intId + "']").closest('tr').index();
			// 	if (that.model.attributes.imageSliderSection.length > index && that.model.attributes.imageSliderSection[index] != undefined) {
			// 			var image = that.model.get('imageSliderSection')[index];
			// 			image.radios = $("#id_radios input[name='radios_slider" + intId + "']:checked").val();
			// 			that.model.get('imageSliderSection').splice(index, 1, image);
			// 			console.log(that.model.attributes.imageSliderSection[index]);
			// 	}
			// });

			$("#video_slider" + intId).on('change', function() {
				var index = $("#video_slider" + intId).closest('tr').index();
				if (that.model.attributes.imageSliderSection.length > index && that.model.attributes.imageSliderSection[index] != undefined) {
						var image = that.model.get('imageSliderSection')[index];
						image.video = $("#video_slider" + intId).val();
						that.model.get('imageSliderSection').splice(index, 1, image);
				}
			});

			that.setUploadable($('#' + inputId), "slider");

		} else {
			$('#image_saved tbody td > div.clearfix').addClass('highlight');
			setTimeout("$('#image_saved tbody td > div.clearfix').removeClass('highlight');", 2000);
		}
	},
	/*
	 * This function will initialize the images input based on the saved
	 * preference
	 */
	initButtonSection: function() {
		var that = this;
		_.each(this.model.get('buttonSection'), function(item, index) {
			var intId = that.buttonsCont;
			var inputId = "btn_file_image" + intId;
			var row = that.createSavedTemplateImageInputRow(intId, item, inputId, "button");

			$("#nav_button_table").append(row);

			// Add spacebar, enter and click to browse button, to trigger file upload
			that.setBrowseButtonTrigger(intId);

			$("#link_button" + intId).on('change', function() {
				var image = that.model.get('buttonSection')[index];
				image.href = $("#link_button" + intId).val();
				that.model.get('buttonSection').splice(index, 1, image);
				image = null;
			});
			
			$("#description_button" + intId).on('change', function() {
				var image = that.model.get('buttonSection')[index];
				image.description = $("#description_button" + intId).val();
				that.model.get('buttonSection').splice(index, 1, image);
				image = null;
			});

			// We make the table sortable
			that.setTableSortable($('#nav_button_table'), that.model.get('buttonSection'));

			// When clicked delete button the object is removed from the model

			$("#del_button" + intId).on('click', function() {
				that.model.attributes.buttonSection.splice($('#' + inputId).closest('tr').index(), 1)
				$.each(that.buttonFiles, function(index, item) {
					if (item.input[0].id.indexOf('#' + inputId) >= 0) {
						that.buttonFiles.splice(index, 1)
						return false;
					}
				});

				$(this).closest("tr").remove();

			});

			that.setUploadable($('#' + inputId), "button");
			that.buttonsCont += 1;
		});

	},
	/*
	 * This function is called when we want to add a new image input. The files
	 * already saved will be stored in image_table, whilst those input that are
	 * created when clicking "add new slide" will be added to image_saved table.
	 * This is done to reduce code complexity when sorting the inputs.
	 */
	addButtonsInput: function() {
		if ($("#nav_button_saved tr").length < 1) {
			var that = this;
			var intId = that.buttonsCont;
			var inputId = "btn_file_image" + intId;
			that.buttonsCont += 1;
			var row = that.createAddTemplateImageInputRow(intId, inputId, "button");

			$("#nav_button_saved").append(row);

			// Add spacebar, enter and click to browse button, to trigger file upload
			this.setBrowseButtonTrigger(intId);


			$("#del_button" + intId).on('click', function() {
				var table = $("#del_button" + intId).closest("table");
				if (table.is("#nav_button_table")) {
					if (($("#nav_button_table tr").length) == that.model.attributes.buttonSection.length) {
						that.model.attributes.buttonSection.splice($('#' + inputId).closest('tr').index(), 1);
					}
					$.each(that.buttonFiles, function(index, item) {
						if (item.input[0].id.indexOf('#' + inputId) >= 0) {
							that.buttonFiles.splice(index, 1)
							return false;
						}
					});
				}
				$(this).closest("tr").remove();
			});
			$("#link_button" + intId).on('change', function() {
				var index = $("#link_button" + intId).closest('tr').index();
				if (that.model.attributes.buttonSection.length > index && that.model.attributes.buttonSection[index] != undefined) {
						var image = that.model.get('buttonSection')[index];
						image.href = $("#link_button" + intId).val();
						that.model.get('buttonSection').splice(index, 1, image);
				}
			});
			
			$("#description_button" + intId).on('change', function() {
				var index = $("#description_button" + intId).closest('tr').index();
				if (that.model.attributes.buttonSection.length > index && that.model.attributes.buttonSection[index] != undefined) {
						var image = that.model.get('buttonSection')[index];
						image.description = $("#description_button" + intId).val();
						that.model.get('buttonSection').splice(index, 1, image);
				}
			});

			that.setUploadable($('#' + inputId), "button");

		} else {
			$('#nav_button_saved tbody td > div.clearfix').addClass('highlight');
			setTimeout("$('#nav_button_saved tbody td > div.clearfix').removeClass('highlight');", 2000);
		}
	},
	setBrowseButtonTrigger: function() {

		$('.imageComponent .crop button').off("keypress").on("keypress", function(e) {
			if (e.which == 32 || e.which == 13) { // spacebar or enter
				e.preventDefault();
				$(this).parent().find('input[type=file]').trigger("click");
			}
		}).on("click", function(e) {
			e.preventDefault();
			$(this).parent().find('input[type=file]').trigger("click");
		});

	},

	setUploadable: function(input, section) {

		input.fileupload({
				url: '/personalizeHome/upload',
				dataType: 'json',
				timeout: 60000,
				acceptFileTypes: /(\.|\/)(gif|jpe?g|png)$/i,
				autoUpload: false,
				add: function(e, data) {
					if (data.files[0].size > 5000000) { // 5mb
						$.gritter.add({
							title: gettext('ADMIN-HOME-SECTION-NOTVALIDURL-TITLE'),
							text: gettext('ADMIN-HOME-SECTION-MAXSIZE-TEXT'),
							image: '/static/workspace/images/common/ic_validationError32.png',
							sticky: false,
							time: 3000
						});
					} else {
						var found = false;
						var files = null
						if(section === "slider"){
								files = that.sliderFiles;
						}
						else{
								files = that.buttonFiles;   
						}
						$.each(files, function(index, item) {
							//check the input whose image is going to be uploades is not already in the list
							if (item.input[0].id.indexOf(input[0]) >= 0) {
								item.file = data
								found = true;
								return false;
							}
						});

						if (!found) {
							files.push({
								"input": data.fileInput,
								"file": data.files
							})
						}

						that.handleFiles(data.files, data.fileInput)
					}
				},
				done: function(e, data) {
					/*
					 * After the file was submitted this function is called to set
					 * image attribute in the model and, then trigger save funciton
					 * if it is the last element in the table
					 *
					 **/

					var input = $("#" + data.fileInput[0].id)
						/* We replace the label for the img src, because we can now display img src due it is
						 *an external source
						 */
					if (window.FileReader === undefined) {
						input.parent().parent().find('label').remove()
						input.parent().parent().before("<img src=" + data.result['url'] + " alt=\"\"class=\"FL\"/>");
					}

					var inputRow = input.closest('tr');
					var inputUrl = inputRow.find("input[type=url]");
					var inputDescription = inputRow.find("input[type=text]");
					var inputVideo = inputRow.find(".video_url");
					var inputRadio = inputRow.find("input[type=radio]:checked");
					var href = '';
					var description = '';
					var video = '';
					var radio = '';
					if (typeof inputUrl.val() != 'undefined') {
						href = inputUrl.val();
					}
					if (typeof inputDescription.val() != 'undefined') {
						description = inputDescription.val();
					}
					if (typeof inputVideo.val() != 'undefined') {
						video = inputVideo.val();
					}
					if (typeof inputRadio.val() != 'undefined') {
						radio = inputRadio.val();
					}
					if (data.fileInput[0].id.indexOf("btn_file_image") >= 0) {
						that.model.get('buttonSection').splice(inputRow.index(), 1, {
							'image': data.result['url'],
							'href': href,
							'description': description,
							'video': video,
							'radio': radio
						});
					} else {
						that.model.get('imageSliderSection').splice(inputRow.index(), 1, {
							'image': data.result['url'],
							'href': href,
							'description': description,
							'video': video,
							'radio': radio
						});
					}

				},

				sequentialUploads: true,
				multipart: true,

			}).bind('fileuploadstart', function(e) {
				$("#ajax_loading_overlay").show();
			})
			.bind('fileuploadstop', function(e) {
				$("#ajax_loading_overlay").hide();
			})
			.bind('fileuploadfail', function(e, data) {
				if (data.errorThrown == "timeout") {
					$.gritter.add({
						title: gettext('ADMIN-HOME-SECTION-ERROR-TITLE'),
						text: gettext('ADMIN-HOME-SECTION-TIMEOUTERROR-TEXT'),
						image: '/static/workspace/images/common/ic_validationError32.png',
						sticky: false,
						time: 3000
					});
				} else {
					$.gritter.add({
						title: gettext('ADMIN-HOME-SECTION-ERROR-TITLE'),
						text: gettext('ADMIN-HOME-SECTION-ERROR-TEXT'),
						image: '/static/workspace/images/common/ic_validationError32.png',
						sticky: false,
						time: 3000
					});
				}

			});
	},
	setTableSortable: function(table, model_element) {
		table.children('tbody').sortable({
			start: function(e, ui) {
				$(this).attr('data-previndex', ui.item.index());
			},
			update: function(e, ui) {
				// We sort the attribute in the model with splice
				var newIndex = ui.item.index();
				var oldIndex = $(this).attr('data-previndex');
				$(this).removeAttr('data-previndex');
				if (model_element != undefined) {
					model_element.splice(newIndex, 0, model_element.splice(oldIndex, 1)[0]);
				}
				table.children('tbody tr').each(function(i, item) {
					var urlInput = $(this).find("input[type=url]");
					var image = model_element[i];
					if (image != undefined && image.href != urlInput.val()) {
						image.href = urlInput.val();
					}
					var descriptionInput = $(this).find("input[type=text]");
					if (image != undefined && image.description != descriptionInput.val()) {
							image.description = descriptionInput.val();
					}
					var videoInput = $(this).find(".video_url");
					if (image != undefined && image.video != videoInput.val()) {
							image.video = videoInput.val();
					}
				});

			}
		});
	},

	initMiddleBottomImage : function () {
		var that = this;

		var middleBottomSectionImageUrl = that.model.attributes.middleBottomSectionImageUrl;

		if (typeof middleBottomSectionImageUrl != 'undefined' && middleBottomSectionImageUrl != '') {
			var img = $('<img>');
			img.attr('src', middleBottomSectionImageUrl);
			$("#id_middleBottomImage").parent().before(img);
			$("#id_btnRemoveMiddleBottom").show();
		}

		// Add spacebar, enter and click to browse button, to trigger file upload
		that.setBrowseButtonTrigger();

		$('#id_middleBottomImage').fileupload({
			url : '/personalizeHome/upload',
			dataType : 'json',
			acceptFileTypes : /(\.|\/)(gif|jpe?g|png)$/i,
			timeout : 60000,
			autoUpload : false,

			add : function (e, data) {
				if (data.files[0].size > 5000000) { // 5mb
					$.gritter.add({
						title : gettext('ADMIN-HOME-SECTION-NOTVALIDURL-TITLE'),
						text : gettext('ADMIN-HOME-SECTION-MAXSIZE-TEXT'),
						image : '/static/workspace/images/common/ic_validationError32.png',
						sticky : false,
						time : 3000
					});
				} else {
					that.middleBottomImage = data
						var fileInput = {
						inputElement : this,
						inputFiles : data.files,
						inputRemove : $("#id_btnRemoveMiddleBottom")
					}
					that.handleFile(fileInput)
					return false;
				}

			},
			done : function (e, data) {
				/* We replace the label for the img src, because we can now display img src due it is
				 *an external source
				 */
				if (window.FileReader === undefined) {
					$("#id_middleBottomImage").parent().parent().find('label').remove()
					$("#id_middleBottomImage").parent().before("<img src=" + data.result['url'] + " alt=\"\"class=\"FL\"/>");
				}

				that.model.set('middleBottomSectionImageUrl', data.result['url']);

			},

			sequentialUploads : true,
			multipart : true,

		}).bind('fileuploadstart', function (e) {
			$("#ajax_loading_overlay").show();
		})
		.bind('fileuploadstop', function (e) {
			$("#ajax_loading_overlay").hide();
		})
		.bind('fileuploadfail', function (e, data) {
			if (data.errorThrown == "timeout") {
				$.gritter.add({
					title : gettext('ADMIN-HOME-SECTION-ERROR-TITLE'),
					text : gettext('ADMIN-HOME-SECTION-TIMEOUTERROR-TEXT'),
					image : '/static/workspace/images/common/ic_validationError32.png',
					sticky : false,
					time : 3000
				});
			} else {
				$.gritter.add({
					title : gettext('ADMIN-HOME-SECTION-ERROR-TITLE'),
					text : gettext('ADMIN-HOME-SECTION-ERROR-TEXT'),
					image : '/static/workspace/images/common/ic_validationError32.png',
					sticky : false,
					time : 3000
				});
			}

		});

	},

	initLeftBottomImage : function () {
		var that = this;

		var leftBottomSectionImageUrl = that.model.attributes.leftBottomSectionImageUrl;

		if (typeof leftBottomSectionImageUrl != 'undefined' && leftBottomSectionImageUrl != '') {
			var img = $('<img>');
			img.attr('src', leftBottomSectionImageUrl);
			$("#id_leftBottomImage").parent().before(img);
			$("#id_btnRemoveLeftBottom").show();
		}

		// Add spacebar, enter and click to browse button, to trigger file upload
		that.setBrowseButtonTrigger();

		$('#id_leftBottomImage').fileupload({
			url : '/personalizeHome/upload',
			dataType : 'json',
			acceptFileTypes : /(\.|\/)(gif|jpe?g|png)$/i,
			timeout : 60000,
			autoUpload : false,

			add : function (e, data) {
				if (data.files[0].size > 5000000) { // 5mb
					$.gritter.add({
						title : gettext('ADMIN-HOME-SECTION-NOTVALIDURL-TITLE'),
						text : gettext('ADMIN-HOME-SECTION-MAXSIZE-TEXT'),
						image : '/static/workspace/images/common/ic_validationError32.png',
						sticky : false,
						time : 3000
					});
				} else {
					that.leftBottomImage = data;
					var fileInput = {
						inputElement : this,
						inputFiles : data.files,
						inputRemove : $("#id_btnRemoveLeftBottom")
					}
					that.handleFile(fileInput)
					return false;
				}

			},
			done : function (e, data) {
				/* We replace the label for the img src, because we can now display img src due it is
				 *an external source
				 */
				if (window.FileReader === undefined) {
					$("#id_leftBottomImage").parent().parent().find('label').remove()
					$("#id_leftBottomImage").parent().before("<img src=" + data.result['url'] + " alt=\"\"class=\"FL\"/>");
				}

				that.model.set('leftBottomSectionImageUrl', data.result['url']);

			},

			sequentialUploads : true,
			multipart : true,

		}).bind('fileuploadstart', function (e) {
			$("#ajax_loading_overlay").show();
		})
		.bind('fileuploadstop', function (e) {
			$("#ajax_loading_overlay").hide();
		})
		.bind('fileuploadfail', function (e, data) {
			if (data.errorThrown == "timeout") {
				$.gritter.add({
					title : gettext('ADMIN-HOME-SECTION-ERROR-TITLE'),
					text : gettext('ADMIN-HOME-SECTION-TIMEOUTERROR-TEXT'),
					image : '/static/workspace/images/common/ic_validationError32.png',
					sticky : false,
					time : 3000
				});
			} else {
				$.gritter.add({
					title : gettext('ADMIN-HOME-SECTION-ERROR-TITLE'),
					text : gettext('ADMIN-HOME-SECTION-ERROR-TEXT'),
					image : '/static/workspace/images/common/ic_validationError32.png',
					sticky : false,
					time : 3000
				});
			}

		});

	},

	initRightBottomImage : function () {
		var that = this;

		var rightBottomSectionImageUrl = that.model.attributes.rightBottomSectionImageUrl;

		if (typeof rightBottomSectionImageUrl != 'undefined' && rightBottomSectionImageUrl != '') {
			var img = $('<img>');
			img.attr('src', rightBottomSectionImageUrl);
			$("#id_rightBottomImage").parent().before(img);
			$("#id_btnRemoveRightBottom").show();
		}

		// Add spacebar, enter and click to browse button, to trigger file upload
		that.setBrowseButtonTrigger();

		$('#id_rightBottomImage').fileupload({
			url : '/personalizeHome/upload',
			dataType : 'json',
			acceptFileTypes : /(\.|\/)(gif|jpe?g|png)$/i,
			timeout : 60000,
			autoUpload : false,

			add : function (e, data) {
				if (data.files[0].size > 5000000) { // 5mb
					$.gritter.add({
						title : gettext('ADMIN-HOME-SECTION-NOTVALIDURL-TITLE'),
						text : gettext('ADMIN-HOME-SECTION-MAXSIZE-TEXT'),
						image : '/static/workspace/images/common/ic_validationError32.png',
						sticky : false,
						time : 3000
					});
				} else {
					that.rightBottomImage = data;
					var fileInput = {
						inputElement : this,
						inputFiles : data.files,
						inputRemove : $("#id_btnRemoveRightBottom")
					}
					that.handleFile(fileInput)
					return false;
				}

			},
			done : function (e, data) {
				/* We replace the label for the img src, because we can now display img src due it is
				 *an external source
				 */
				if (window.FileReader === undefined) {
					$("#id_rightBottomImage").parent().parent().find('label').remove()
					$("#id_rightBottomImage").parent().before("<img src=" + data.result['url'] + " alt=\"\"class=\"FL\"/>");
				}

				that.model.set('rightBottomSectionImageUrl', data.result['url']);

			},

			sequentialUploads : true,
			multipart : true,

		}).bind('fileuploadstart', function (e) {
			$("#ajax_loading_overlay").show();
		})
		.bind('fileuploadstop', function (e) {
			$("#ajax_loading_overlay").hide();
		})
		.bind('fileuploadfail', function (e, data) {
			if (data.errorThrown == "timeout") {
				$.gritter.add({
					title : gettext('ADMIN-HOME-SECTION-ERROR-TITLE'),
					text : gettext('ADMIN-HOME-SECTION-TIMEOUTERROR-TEXT'),
					image : '/static/workspace/images/common/ic_validationError32.png',
					sticky : false,
					time : 3000
				});
			} else {
				$.gritter.add({
					title : gettext('ADMIN-HOME-SECTION-ERROR-TITLE'),
					text : gettext('ADMIN-HOME-SECTION-ERROR-TEXT'),
					image : '/static/workspace/images/common/ic_validationError32.png',
					sticky : false,
					time : 3000
				});
			}

		});

	},

	handleFile : function (fileInput) {
		var img;
		var files = fileInput.inputFiles;
		var inputElement = fileInput.inputElement;
		var btnRemoveElement = fileInput.inputRemove;
		for (var i = 0; i < files.length; i++) {
			var file = files[i];
			/*
			 * This code checks if browser has filereadar, and if it doesn't (IE <10) it will display
			 * a label with filename instead
			 * */
			var imageField = $(inputElement).parent().parent().find('img')
				if (window.FileReader) {
					if (!imageField.length > 0) {
						img = document.createElement("img");
						$(btnRemoveElement).show();
					} else {
						img = imageField[0]
					}
					img.classList.add("obj");
					img.file = file;
					$(inputElement).parent().before(img);
					var reader = new FileReader();
					reader.onload = (function (aImg) {
						return function (e) {
							aImg.src = e.target.result;
						};
					})(img);
					reader.readAsDataURL(file);

				} else {
					var labelField = $(inputElement).parent().parent().find('label')
						$(btnRemoveElement).show();
					if (imageField.length > 0) {
						$(imageField.remove())
						labelField = $("<label>").text(file.name);
					} else {

						if (labelField.length > 0) {
							$(labelField).text(file.name)
						} else {
							labelField = $("<label>").text(file.name);
						}
					}

					$(inputElement).parent().before(labelField);
				}
		}
	},

	handleFiles: function(files, event) {
		var input = event[0].id
		var img
		for (var i = 0; i < files.length; i++) {
			var file = files[i];
			/*
			 * This code checks if browser has filereadar, and if it doesn't (IE <10) it will display
			 * a label with filename
			 * */
			var imageField = $("#" + input).parent().parent().find('img')
			if (window.FileReader) {
				if (!imageField.length > 0) {
					img = document.createElement("img");
				} else {
					img = imageField[0]
				}
				img.className += " obj";
				img.file = file;
				$("#" + input).parents('.crop').before(img);

				var reader = new FileReader();
				reader.onload = (function(aImg) {
					return function(e) {
						aImg.src = e.target.result;
					};
				})(img);
				reader.readAsDataURL(file);

			} else {
				var labelField = $("#" + input).parent().parent().find('label')
				if (imageField.length > 0) {
					imageField.remove()
					labelField = $("<label>").text(file.name);
				} else {

					if (labelField.length > 0) {
						$(labelField).text(file.name)
					} else {
						labelField = $("<label>").text(file.name);
					}
				}

				$("#" + input).parents('.crop').before(labelField);
			}

			var table = $("#" + input).closest("table");

			// When we choose a file, we remove the input from the image_save
			// table and move it to image_table
			if (table.is("#image_saved")) {
				that.model.get('imageSliderSection').push("");
				var row = $("#" + input).closest("tr");
				row.detach();

				$("#image_table").append(row);
				var tdSort = '<td class=\"draggableSection\"><i class=\"arrangeIcon\"></i></td>'
				$('#image_table tr:last td:eq(0)').before(tdSort);
				this.setTableSortable($("#image_table"), that.model.get('imageSliderSection'));
			} else if (table.is("#nav_button_saved")) {
				that.model.get('buttonSection').push("");
				var row = $("#" + input).closest("tr");
				row.detach();

				$("#nav_button_table").append(row);
				var tdSort = '<td class=\"draggableSection\"><i class=\"arrangeIcon\"></i></td>'
				$('#nav_button_table tr:last td:eq(0)').before(tdSort);
				this.setTableSortable($("#nav_button_table"), that.model.get('buttonSection'));
			}
		}

	},

	removeLeftBottomImage : function () {
		if (this.model.get('leftBottomSectionImageUrl') != undefined) {
			this.model.set('leftBottomSectionImageUrl', undefined);
		}
		var deleteBtn = $("#id_btnRemoveLeftBottom")
			var imageField = deleteBtn.parent().parent().find('img')

			if (false) {
				imageField.remove();
			} else {
				var labelField = deleteBtn.parent().find('label')
					if (imageField.length > 0) {
						imageField.remove()
					} else {
						if (labelField.length > 0) {
							labelField.remove();
						}
					}
			}
			deleteBtn.hide();
	},

	removeMiddleBottomImage : function () {
		if (this.model.get('middleBottomSectionImageUrl') != undefined) {
			this.model.set('middleBottomSectionImageUrl', undefined);
		}
		var deleteBtn = $("#id_btnRemoveMiddleBottom")
			var imageField = deleteBtn.parent().parent().find('img')

			if (false) {
				imageField.remove();
			} else {
				var labelField = deleteBtn.parent().find('label')
					if (imageField.length > 0) {
						imageField.remove()
					} else {
						if (labelField.length > 0) {
							labelField.remove();
						}
					}
			}
			deleteBtn.hide();
	},

	removeRightBottomImage : function () {
		if (this.model.get('rightBottomSectionImageUrl') != undefined) {
			this.model.set('rightBottomSectionImageUrl', undefined);
		}
		var deleteBtn = $("#id_btnRemoveRightBottom")
			var imageField = deleteBtn.parent().parent().find('img')

			if (false) {
				imageField.remove();
			} else {
				var labelField = deleteBtn.parent().find('label')
					if (imageField.length > 0) {
						imageField.remove()
					} else {
						if (labelField.length > 0) {
							labelField.remove();
						}
					}
			}
			deleteBtn.hide();
	},

	validateUrl: function() {

		$('.complete_url').validate({
			rules: {
				complete_url: true
			}
		});

	},
	save: function(event) {
		that = this;

		this.calculateButtonRowWidth();
		
		$.validator.addClassRules("requiredText", {
			required: true,
			minlength: 1
		});

		this.$el.parent().validate({

			rules: {
				id_buttonsPerRow: {
					number: true
				}
			},

			invalidHandler: function(event, validator) {

				var i = 0;
				for (i = 0; i < validator.invalidElements().length; i++) {
					//If the name is id_buttonsPerRow, then we display error message for non numeric
					if ($(validator.invalidElements()[i]).attr('name') == 'id_buttonsPerRow') {
						$.gritter.add({
							title: gettext('ADMIN-HOME-SECTION-NOTVALIDURL-TITLE'),
							text: gettext('ADMIN-HOME-SECTION-NOTVALIDNUM-TEXT'),
							image: '/static/workspace/images/common/ic_validationError32.png',
							sticky: false,
							time: 5000
						});
					} else {

						$.gritter.add({
							title: gettext('ADMIN-HOME-SECTION-ERROR-TITLE'),
							text: gettext('ADMIN-HOME-SECTION-EMPTY-TEXT'),
							image: '/static/workspace/images/common/ic_validationError32.png',
							sticky: false,
							time: 5000
						});
					}

				}

			}

		});
		if ($('.complete_url').length > 0) {
			// set validate URL
			this.validateUrl();

			if ($(".complete_url").valid()) {
				var ajaxReqs = [];
				//We push the request into an array
				_.each(that.sliderFiles, function(item, index) {
					ajaxReqs.push($("#" + item['input'][0].id).fileupload('send', {
						fileInput: item['input'],
						files: item['file']
					}));
				})

				_.each(that.buttonFiles, function(item, index) {
					ajaxReqs.push($("#" + item['input'][0].id).fileupload('send', {
						fileInput: item['input'],
						files: item['file']
					}));
				})

				if (typeof that.leftBottomImage != 'undefined' && that.leftBottomImage != '') {
					ajaxReqs.push($("#id_leftBottomImage").fileupload('send', {
							fileInput : that.leftBottomImage.fileInput,
							files : that.leftBottomImage.files
						}));
				}

				if (typeof that.rightBottomImage != 'undefined' && that.rightBottomImage != '') {
					ajaxReqs.push($("#id_rightBottomImage").fileupload('send', {
							fileInput : that.rightBottomImage.fileInput,
							files : that.rightBottomImage.files
						}));
				}
				if (typeof that.middleBottomImage != 'undefined' && that.middleBottomImage != '') {
					ajaxReqs.push($("#id_middleBottomImage").fileupload('send', {
							fileInput : that.middleBottomImage.fileInput,
							files : that.middleBottomImage.files
						}));
				}

				if (that.sliderFiles.length > 0 || that.buttonFiles.length > 0) {
					//We loop through the request, once the all the ajax calls are done, we trigger the save preference
					$.when.apply($, ajaxReqs).then(function() {
						that.sliderFiles = [];
						that.buttonFiles = [];
						that.savePreference(event);
					})
				} else {
					$.when.apply($, ajaxReqs).then(function() {
						that.savePreference(event);
					});
				}
			} else {
				$.gritter.add({
					title: gettext('ADMIN-HOME-SECTION-NOTVALIDURL-TITLE'),
					text: gettext('ADMIN-HOME-SECTION-NOTVALIDURL-TEXT'),
					image: '/static/workspace/images/common/ic_validationError32.png',
					sticky: false,
					time: 5000
				});
			}
		} else {
			this.savePreference(event);
		}
	},

	savePreference: function(event) {
		var btn_id = $(event.currentTarget).attr("id");
		var ob = {};
		if (btn_id === 'id_save' || btn_id === 'id_save_top') {
            this.currentModel.attributes.config = this.model.toJSON();
            this.currentModel.attributes.themeID = '6';
            ob['config'] = this.currentModel.attributes.config;
            ob['theme'] = this.currentModel.attributes.themeID;
			ob['type'] = 'save';
		} else {
			ob['config'] = this.model.toJSON();
			ob['theme'] = '6';
			ob['type'] = 'preview';
		}
		$.ajax({
			type: 'POST',
			data: {
				'jsonString': saferStringify(ob)
			},
			dataType: 'json',
			beforeSend: function(xhr, settings) {
				// call global beforeSend func
                $.ajaxSettings.beforeSend(xhr, settings);
                
				$("#ajax_loading_overlay").show();
			},
			success: function(response) {
				$("#ajax_loading_overlay").hide();
				if (btn_id === "id_save" || btn_id === 'id_save_top') {
					$.gritter.add({
						title: gettext('ADMIN-HOME-SECTION-SUCCESS-TITLE'),
						text: gettext('ADMIN-HOME-SECTION-SUCCESS-TEXT'),
						image: '/static/workspace/images/common/ic_validationOk32.png',
						sticky: false,
						time: 3500
					});
				} else {
					event.preventDefault();
					var preview_home = response['preview_home']
					window.open(preview_home, '', 'width=1024,height=500,resizable=yes,scrollbars=yes');
				}

			},
			error: function(response) {
				$("#ajax_loading_overlay").hide();
				$.gritter.add({
					title: gettext('ADMIN-HOME-SECTION-ERROR-TITLE'),
					text: gettext('ADMIN-HOME-SECTION-ERROR-TEXT'),
					image: '/static/workspace/images/common/ic_validationError32.png',
					sticky: true,
					time: 3000
				});
			},
			url: '/personalizeHome/save/'
		});


	},

	calculateButtonRowWidth: function() {
		var that = this;

		var btnsPerRow = $("#id_buttonsPerRow").val();

		// If no value is set, the default value (20) will be set as row width
		if (btnsPerRow) {
			that.model.set('buttonsPerRowWidth', (100 / btnsPerRow).toString() );
		}			

	},

	onRadioChange: function(event) {
		var value = $(event.currentTarget).val();
		$(event.currentTarget).parents(".sliderData").find(".radioSection").hide();
		$(event.currentTarget).parents(".sliderData").find("." + value).show();
	}

});