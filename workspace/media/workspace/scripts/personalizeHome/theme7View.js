var theme7View = Backbone.Epoxy.View.extend({
	el: '#id_themeForm',
	template: null,
	welcomeImage : "",
	sliderFiles: [],
	prioritiesSliderFiles: [],
	buttonFiles: [],
	sliderInputCont: 0,
	prioritiesSliderInputCont: 0,
	buttonsCont: 0,
	middleBottomImage : "",
	leftBottomImage : "",
	rightBottomImage : "",
	linksCont : 0,

	events: {
		"click .featuredSection #id_new_slide": "addSliderInput",
		"click .prioritiesSection #id_new_slide": "addPrioritiesSliderInput",
		"click #id_new_button": "addButtonsInput",
		"click #id_btnRemoveWelcome" : "removeWelcomeImage",
		"click #id_btnRemoveLeftBottom" : "removeLeftBottomImage",
		"click #id_btnRemoveMiddleBottom" : "removeMiddleBottomImage",
		"click #id_btnRemoveRightBottom" : "removeRightBottomImage",
		"change #id_radios input[type='radio']": "onRadioChange",
		"click #id_new_link" : "addLinksInput",
		"click #links_section tr .remove" : "removeRow"
	},

	initialize: function(options) {

		this.currentView = options.currentView;
        this.currentModel = options.currentModel;

		this.currentView.helpAndTips('hide');
		that = this;
		this.template = _.template($("#id_theme7Template").html());
		this.render();
		this.initWelcomeImage();
		this.initSliderSection();
		this.initPrioritiesSliderSection();
		this.initButtonSection();
		this.initMiddleBottomImage();
		this.initLeftBottomImage();
		this.initRightBottomImage();
		this.initLinksSection();
		this.colorPicker();
	},

	render: function() {
		this.$el.html(this.template(this.model.attributes));
		return this;
	},
	createAddTemplateSliderInputRow: function(intId, inputId, section) {
		var linkText = gettext('ADMIN-HOME-SECTION-LINKTEXT');
		var deleteText = gettext('ADMIN-HOME-SECTION-DELETESLIDE');
		var titleLabelText = gettext('ADMIN-HOME-SECTION-TITLE-LABEL');
		var titlePlaceHolderText = gettext('ADMIN-HOME-SECTION-TITLE-TEXT');
		var placeholderText = gettext('ADMIN-HOME-SECTION-LINKPLACEHOLDER');
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
								'<label for=\"title_' + section + intId + '\" class=\"FL\">' + titleLabelText + '</label>' +
								'<div class=\"formErrorMessageContainer FL\">' +
									'<input type=\"text\" maxlength="50" id=\"title_' + section + intId + '\" name=\"title_' + section + intId + '\" class=\"field FL requiredText\" placeholder=\"' + titlePlaceHolderText + '\"/>' +
								'</div>' +
							'</div>' +

							'<div class=\"clearfix linkSection radioSection\">' +
								'<label for=\"link_' + intId + '\"class=\"FL\">' + linkText + ':</label>' +
								'<div class=\"formErrorMessageContainer FL\">' +
									'<input type=\"url\" id=\"link_' + section + intId + '\" class=\"field FL urlLink complete_url\" placeholder=\"' + placeholderText + '\"/>' +
								'</div>' +
							'</div>' +

						'</div>' +

					'</div>' +
				'</td>' +
			'</tr>';
		return html;
	},
	createAddTemplateImageInputRow: function(intId, inputId, section) {
		var linkText = gettext('ADMIN-HOME-SECTION-LINKTEXT');
		var deleteText = gettext('ADMIN-HOME-SECTION-DELETESLIDE');
		var titleLabelText = gettext('ADMIN-HOME-SECTION-TITLE-LABEL');
		var titlePlaceHolderText = gettext('ADMIN-HOME-SECTION-TITLE-TEXT');
		var descriptionLabelText = gettext('APP-DESCRIPTION2-LABEL');
		var descriptionPlaceHolderText = gettext('APP-DESCRIPTION2-TEXT');
		var placeholderText = gettext('ADMIN-HOME-SECTION-LINKPLACEHOLDER');
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
								'<label for=\"title_' + section + intId + '\" class=\"FL\">' + titleLabelText + '</label>' +
								'<div class=\"formErrorMessageContainer FL\">' +
									'<input type=\"text\" id=\"title_' + section + intId + '\" name=\"title_' + section + intId + '\" class=\"field FL requiredText\" placeholder=\"' + titlePlaceHolderText + '\" maxlength="55" />' +
								'</div>' +
							'</div>' +

							'<div class=\"clearfix rowSeparation\">' +
								'<label for=\"description_' + section + intId + '\" class=\"FL\">' + descriptionLabelText + '</label>' +
								'<div class=\"formErrorMessageContainer FL\">' +
									'<input type=\"text\" id=\"description_' + section + intId + '\" name=\"description_' + section + intId + '\" class=\"field FL requiredText\" placeholder=\"' + descriptionPlaceHolderText + '\" maxlength="150" />' +
								'</div>' +
							'</div>' +

							'<div class=\"clearfix linkSection radioSection\">' +
								'<label for=\"link_' + intId + '\"class=\"FL\">' + linkText + ':</label>' +
								'<div class=\"formErrorMessageContainer FL\">' +
									'<input type=\"url\" id=\"link_' + section + intId + '\" class=\"field FL urlLink complete_url\" placeholder=\"' + placeholderText + '\"/>' +
								'</div>' +
							'</div>' +

						'</div>' +

					'</div>' +
				'</td>' +
			'</tr>';
		return html;
	},
	createAddTemplatePrioritiesInputRow: function(intId, inputId, section) {
		var linkText = gettext('ADMIN-HOME-SECTION-LINKTEXT');
		var deleteText = gettext('ADMIN-HOME-SECTION-DELETESLIDE');
		var titleLabelText = gettext('ADMIN-HOME-SECTION-TITLE-LABEL');
		var titlePlaceHolderText = gettext('ADMIN-HOME-SECTION-TITLE-TEXT');
		var descriptionLabelText = gettext('APP-DESCRIPTION2-LABEL');
		var descriptionPlaceHolderText = gettext('APP-DESCRIPTION2-TEXT');
		var placeholderText = gettext('ADMIN-HOME-SECTION-LINKPLACEHOLDER');
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
								'<label for=\"title_' + section + intId + '\" class=\"FL\">' + titleLabelText + '</label>' +
								'<div class=\"formErrorMessageContainer FL\">' +
									'<input type=\"text\" id=\"title_' + section + intId + '\" name=\"title_' + section + intId + '\" class=\"field FL requiredText\" placeholder=\"' + titlePlaceHolderText + '\"/>' +
								'</div>' +
							'</div>' +

							'<div class=\"clearfix rowSeparation\">' +
								'<label for=\"description_' + section + intId + '\" class=\"FL\">' + descriptionLabelText + '</label>' +
								'<div class=\"formErrorMessageContainer FL\">' +
									'<input type=\"text\" id=\"description_' + section + intId + '\" name=\"description_' + section + intId + '\" class=\"field FL requiredText\" placeholder=\"' + descriptionPlaceHolderText + '\"/>' +
								'</div>' +
							'</div>' +

							'<div class=\"clearfix linkSection radioSection\">' +
								'<label for=\"link_' + intId + '\"class=\"FL\">' + linkText + ':</label>' +
								'<div class=\"formErrorMessageContainer FL\">' +
									'<input type=\"url\" id=\"link_' + section + intId + '\" class=\"field FL urlLink complete_url\" placeholder=\"' + placeholderText + '\"/>' +
								'</div>' +
							'</div>' +

						'</div>' +

					'</div>' +
				'</td>' +
			'</tr>';
		return html;
	},
	createSavedTemplateSliderInputRow: function(rowIndex, item, inputId, section) {
		var linkText = gettext('ADMIN-HOME-SECTION-LINKTEXT');
		var deleteText = gettext('ADMIN-HOME-SECTION-DELETESLIDE');
		var titleLabelText = gettext('ADMIN-HOME-SECTION-TITLE-LABEL');
		var titlePlaceHolderText = gettext('ADMIN-HOME-SECTION-TITLE-TEXT');
		var placeholderText = gettext('ADMIN-HOME-SECTION-LINKPLACEHOLDER');
		var buttonText = gettext('ADMIN-HOME-SECTION-BUTTONTEXT');

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
								'<label for=\"title_' + section + rowIndex + '\" class=\"FL\">' + titleLabelText + '</label>' +
								'<div class=\"formErrorMessageContainer FL\">' +
									'<input type=\"text\" maxlength="50" id=\"title_' + section + rowIndex + '\" value=\"' + item.title + '\" name=\"title_' + section + rowIndex + '\" class=\"field FL requiredText\" placeholder=\"' + titlePlaceHolderText + '\"/>' +
								'</div>' +
							'</div>' +

							'<div class=\"clearfix linkSection radioSection\">' +
								'<label for=\"link_' + section + rowIndex + '\" class=\"FL\">' + linkText + ':</label>' +
								'<div class=\"formErrorMessageContainer FL\">' +
									'<input type=\"url\" id=\"link_' + section + rowIndex + '\" value=\"' + item.href + '\" class=\"field FL urlLink complete_url\" placeholder=\"' + placeholderText + '\"/>' +
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
		var titleLabelText = gettext('ADMIN-HOME-SECTION-TITLE-LABEL');
		var titlePlaceHolderText = gettext('ADMIN-HOME-SECTION-TITLE-TEXT');
		var descriptionLabelText = gettext('APP-DESCRIPTION2-LABEL');
		var descriptionPlaceHolderText = gettext('APP-DESCRIPTION2-TEXT');
		var placeholderText = gettext('ADMIN-HOME-SECTION-LINKPLACEHOLDER');
		var buttonText = gettext('ADMIN-HOME-SECTION-BUTTONTEXT');

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
								'<label for=\"title_' + section + rowIndex + '\" class=\"FL\">' + titleLabelText + '</label>' +
								'<div class=\"formErrorMessageContainer FL\">' +
									'<input type=\"text\" id=\"title_' + section + rowIndex + '\" value=\"' + item.title + '\" name=\"title_' + section + rowIndex + '\" class=\"field FL requiredText\" placeholder=\"' + titlePlaceHolderText + '\" maxlength="55" />' +
								'</div>' +
							'</div>' +

							'<div class=\"clearfix rowSeparation\">' +
								'<label for=\"description_' + section + rowIndex + '\" class=\"FL\">' + descriptionLabelText + '</label>' +
								'<div class=\"formErrorMessageContainer FL\">' +
									'<input type=\"text\" id=\"description_' + section + rowIndex + '\" value=\"' + item.description + '\" name=\"description_' + section + rowIndex + '\" class=\"field FL requiredText\" placeholder=\"' + descriptionPlaceHolderText + '\" maxlength="150" />' +
								'</div>' +
							'</div>' +

							'<div class=\"clearfix linkSection radioSection\">' +
								'<label for=\"link_' + section + rowIndex + '\" class=\"FL\">' + linkText + ':</label>' +
								'<div class=\"formErrorMessageContainer FL\">' +
									'<input type=\"url\" id=\"link_' + section + rowIndex + '\" value=\"' + item.href + '\" class=\"field FL urlLink complete_url\" placeholder=\"' + placeholderText + '\"/>' +
								'</div>' +
							'</div>' +

						'</div>' +

					'</div>' +
				'</td>' +
			'</tr>';
		return html;
	},
	createSavedTemplatePrioritiesInputRow: function(rowIndex, item, inputId, section) {
		var linkText = gettext('ADMIN-HOME-SECTION-LINKTEXT');
		var deleteText = gettext('ADMIN-HOME-SECTION-DELETESLIDE');
		var titleLabelText = gettext('ADMIN-HOME-SECTION-TITLE-LABEL');
		var titlePlaceHolderText = gettext('ADMIN-HOME-SECTION-TITLE-TEXT');
		var descriptionLabelText = gettext('APP-DESCRIPTION2-LABEL');
		var descriptionPlaceHolderText = gettext('APP-DESCRIPTION2-TEXT');
		var placeholderText = gettext('ADMIN-HOME-SECTION-LINKPLACEHOLDER');
		var buttonText = gettext('ADMIN-HOME-SECTION-BUTTONTEXT');

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
								'<label for=\"title_' + section + rowIndex + '\" class=\"FL\">' + titleLabelText + '</label>' +
								'<div class=\"formErrorMessageContainer FL\">' +
									'<input type=\"text\" id=\"title_' + section + rowIndex + '\" value=\"' + item.title + '\" name=\"title_' + section + rowIndex + '\" class=\"field FL requiredText\" placeholder=\"' + titlePlaceHolderText + '\"/>' +
								'</div>' +
							'</div>' +

							'<div class=\"clearfix rowSeparation\">' +
								'<label for=\"description_' + section + rowIndex + '\" class=\"FL\">' + descriptionLabelText + '</label>' +
								'<div class=\"formErrorMessageContainer FL\">' +
									'<input type=\"text\" id=\"description_' + section + rowIndex + '\" value=\"' + item.description + '\" name=\"description_' + section + rowIndex + '\" class=\"field FL requiredText\" placeholder=\"' + descriptionPlaceHolderText + '\"/>' +
								'</div>' +
							'</div>' +

							'<div class=\"clearfix linkSection radioSection\">' +
								'<label for=\"link_' + section + rowIndex + '\" class=\"FL\">' + linkText + ':</label>' +
								'<div class=\"formErrorMessageContainer FL\">' +
									'<input type=\"url\" id=\"link_' + section + rowIndex + '\" value=\"' + item.href + '\" class=\"field FL urlLink complete_url\" placeholder=\"' + placeholderText + '\"/>' +
								'</div>' +
							'</div>' +

						'</div>' +

					'</div>' +
				'</td>' +
			'</tr>';
		return html;
	},

	initWelcomeImage : function () {
		var that = this;

		var welcomeSectionImageUrl = that.model.attributes.welcomeSectionImageUrl;
		
		$('#id_welcome_background_color').val(that.model.get('welcomeSectionBackgroundColor'));

		if (typeof welcomeSectionImageUrl != 'undefined' && welcomeSectionImageUrl != '') {
			var img = $('<img>');
			img.attr('src', welcomeSectionImageUrl);
			$("#id_welcomeImage").parent().before(img);
			$("#id_btnRemoveWelcome").show();
		}

		// Add spacebar, enter and click to browse button, to trigger file upload
		that.setBrowseButtonTrigger();

		$('#id_welcomeImage').fileupload({
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
					that.welcomeImage = data;
					var fileInput = {
						inputElement : this,
						inputFiles : data.files,
						inputRemove : $("#id_btnRemoveWelcome")
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
					$("#id_welcomeImage").parent().parent().find('label').remove()
					$("#id_welcomeImage").parent().before("<img src=" + data.result['url'] + " alt=\"\"class=\"FL\"/>");
				}

				that.model.set('welcomeSectionImageUrl', data.result['url']);

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

	/*
	 * This function will initialize the images input based on the saved
	 * preference
	 */
	initSliderSection: function() {
		var that = this;
		
		$('#id_featured_background_color').val(that.model.get('featuredSliderSectionBackgroundColor'));

		_.each(this.model.get('imageSliderSection'), function(item, index) {
			var intId = that.sliderInputCont;
			var inputId = "file_image" + intId;
			var row = that.createSavedTemplateSliderInputRow(intId, item, inputId, "slider");

			$(".featuredSection #image_table").append(row);

			// Add spacebar, enter and click to browse button, to trigger file upload
			that.setBrowseButtonTrigger(intId);

			$(".featuredSection #link_slider" + intId).on('change', function() {
				var image = that.model.get('imageSliderSection')[index];
				image.href = $(".featuredSection #link_slider" + intId).val();
				that.model.get('imageSliderSection').splice(index, 1, image);
				image = null;
			});

			$(".featuredSection #title_slider" + intId).on('change', function() {
					var image = that.model.get('imageSliderSection')[index];
					image.title = $(".featuredSection #title_slider" + intId).val();
					that.model.get('imageSliderSection').splice(index, 1, image);
					image = null;
			});

			// We make the table sortable
			that.setTableSortable($('.featuredSection #image_table'), that.model.get('imageSliderSection'));


			// When clicked delete button the object is removed from the model

			$(".featuredSection #del_slider" + intId).on('click', function() {
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

	addSliderInput: function() {
		if ($(".featuredSection #image_saved tr").length < 1) {
			var that = this;
			var intId = that.sliderInputCont;
			var inputId = "file_image" + intId;
			that.sliderInputCont += 1;
			var row = that.createAddTemplateSliderInputRow(intId, inputId, "slider");

			$(".featuredSection #image_saved").append(row);

			// Add spacebar, enter and click to browse button, to trigger file upload
			this.setBrowseButtonTrigger(intId);

			$(".featuredSection #del_slider" + intId).on('click', function() {
				var table = $(".featuredSection #del_slider" + intId).closest("table");
				if (table.is(".featuredSection #image_table")) {
					if (($(".featuredSection #image_table tr").length) == that.model.attributes.imageSliderSection.length) {
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

			$(".featuredSection #link_slider" + intId).on('change', function() {
				var index = $(".featuredSection #link_slider" + intId).closest('tr').index();
				if (that.model.attributes.imageSliderSection.length > index && that.model.attributes.imageSliderSection[index] != undefined) {
					var image = that.model.get('imageSliderSection')[index];
					image.href = $(".featuredSection #link_slider" + intId).val();
					that.model.get('imageSliderSection').splice(index, 1, image);
				}
			});

			$(".featuredSection #title_slider" + intId).on('change', function() {
				var index = $(".featuredSection #title_slider" + intId).closest('tr').index();
				if (that.model.attributes.imageSliderSection.length > index && that.model.attributes.imageSliderSection[index] != undefined) {
						var image = that.model.get('imageSliderSection')[index];
						image.title = $(".featuredSection #title_slider" + intId).val();
						that.model.get('imageSliderSection').splice(index, 1, image);
				}
			});

			that.setUploadable($('#' + inputId), "slider");

		} else {
			$('.featuredSection #image_saved tbody td > div.clearfix').addClass('highlight');
			setTimeout("$('.featuredSection #image_saved tbody td > div.clearfix').removeClass('highlight');", 2000);
		}
	},

	initPrioritiesSliderSection: function() {
		var that = this;
		
		$('#id_priorities_background_color').val(that.model.get('prioritiesSliderSectionBackgroundColor'));

		_.each(this.model.get('prioritiesSliderSection'), function(item, index) {
			var intId = that.prioritiesSliderInputCont;
			var inputId = "priorities_file" + intId;
			var row = that.createSavedTemplatePrioritiesInputRow(intId, item, inputId, "prioritiesSlider");

			$(".prioritiesSection #image_table").append(row);

			// Add spacebar, enter and click to browse button, to trigger file upload
			that.setBrowseButtonTrigger(intId);

			$(".prioritiesSection #title_prioritiesSlider" + intId).on('change', function() {
					var image = that.model.get('prioritiesSliderSection')[index];
					image.title = $(".prioritiesSection #title_prioritiesSlider" + intId).val();
					that.model.get('prioritiesSliderSection').splice(index, 1, image);
					image = null;
			});

			$(".prioritiesSection #description_prioritiesSlider" + intId).on('change', function() {
					var image = that.model.get('prioritiesSliderSection')[index];
					image.description = $(".prioritiesSection #description_prioritiesSlider" + intId).val();
					that.model.get('prioritiesSliderSection').splice(index, 1, image);
					image = null;
			});

			$(".prioritiesSection #link_prioritiesSlider" + intId).on('change', function() {
				var image = that.model.get('prioritiesSliderSection')[index];
				image.href = $(".prioritiesSection #link_prioritiesSlider" + intId).val();
				that.model.get('prioritiesSliderSection').splice(index, 1, image);
				image = null;
			});

			// We make the table sortable
			that.setTableSortable($('.prioritiesSection #image_table'), that.model.get('prioritiesSliderSection'));


			// When clicked delete button the object is removed from the model

			$(".prioritiesSection #del_prioritiesSlider" + intId).on('click', function() {
				that.model.attributes.prioritiesSliderSection.splice($('#' + inputId).closest('tr').index(), 1)
				$.each(that.prioritiesSliderFiles, function(index, item) {
					if (item.input[0].id.indexOf('#' + inputId) >= 0) {
						that.prioritiesSliderFiles.splice(index, 1)
						return false;
					}
				});

				$(this).closest("tr").remove();

			});
			that.setUploadable($('#' + inputId), "prioritiesSlider");
			that.prioritiesSliderInputCont += 1;
		});

	},

	addPrioritiesSliderInput: function() {
		if ($(".prioritiesSection #image_saved tr").length < 1) {
			var that = this;
			var intId = that.prioritiesSliderInputCont;
			var inputId = "priorities_file" + intId;
			that.prioritiesSliderInputCont += 1;
			var row = that.createAddTemplatePrioritiesInputRow(intId, inputId, "prioritiesSlider");

			$(".prioritiesSection #image_saved").append(row);

			// Add spacebar, enter and click to browse button, to trigger file upload
			this.setBrowseButtonTrigger(intId);

			$(".prioritiesSection #del_prioritiesSlider" + intId).on('click', function() {
				var table = $(".prioritiesSection #del_prioritiesSlider" + intId).closest("table");
				if (table.is(".prioritiesSection #image_table")) {
					if (($(".prioritiesSection #image_table tr").length) == that.model.attributes.prioritiesSliderSection.length) {
						that.model.attributes.prioritiesSliderSection.splice($('#' + inputId).closest('tr').index(), 1);
					}
					$.each(that.prioritiesSliderFiles, function(index, item) {
						if (item.input[0].id.indexOf('#' + inputId) >= 0) {
							that.prioritiesSliderFiles.splice(index, 1)
							return false;
						}
					});
				}
				$(this).closest("tr").remove();
			});

			$(".prioritiesSection #title_prioritiesSlider" + intId).on('change', function() {
				var index = $(".prioritiesSection #title_prioritiesSlider" + intId).closest('tr').index();
				if (that.model.attributes.prioritiesSliderSection.length > index && that.model.attributes.prioritiesSliderSection[index] != undefined) {
						var image = that.model.get('prioritiesSliderSection')[index];
						image.title = $(".prioritiesSection #title_prioritiesSlider" + intId).val();
						that.model.get('prioritiesSliderSection').splice(index, 1, image);
				}
			});

			$(".prioritiesSection #description_prioritiesSlider" + intId).on('change', function() {
				var index = $(".prioritiesSection #description_prioritiesSlider" + intId).closest('tr').index();
				if (that.model.attributes.prioritiesSliderSection.length > index && that.model.attributes.prioritiesSliderSection[index] != undefined) {
						var image = that.model.get('prioritiesSliderSection')[index];
						image.description = $(".prioritiesSection #description_prioritiesSlider" + intId).val();
						that.model.get('prioritiesSliderSection').splice(index, 1, image);
				}
			});

			$(".prioritiesSection #link_prioritiesSlider" + intId).on('change', function() {
				var index = $(".prioritiesSection #link_prioritiesSlider" + intId).closest('tr').index();
				if (that.model.attributes.prioritiesSliderSection.length > index && that.model.attributes.prioritiesSliderSection[index] != undefined) {
					var image = that.model.get('prioritiesSliderSection')[index];
					image.href = $(".prioritiesSection #link_prioritiesSlider" + intId).val();
					that.model.get('prioritiesSliderSection').splice(index, 1, image);
				}
			});

			that.setUploadable($('#' + inputId), "prioritiesSlider");

		} else {
			$('.prioritiesSection #image_saved tbody td > div.clearfix').addClass('highlight');
			setTimeout("$('.prioritiesSection #image_saved tbody td > div.clearfix').removeClass('highlight');", 2000);
		}
	},

	/*
	 * This function will initialize the images input based on the saved
	 * preference
	 */
	initButtonSection: function() {
		var that = this;
		
		$('#id_buttons_background_color').val(that.model.get('buttonSectionBackgroundColor'));

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
			
			$("#title_button" + intId).on('change', function() {
				var image = that.model.get('buttonSection')[index];
				image.title = $("#title_button" + intId).val();
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
			
			$("#title_button" + intId).on('change', function() {
				var index = $("#title_button" + intId).closest('tr').index();
				if (that.model.attributes.buttonSection.length > index && that.model.attributes.buttonSection[index] != undefined) {
						var image = that.model.get('buttonSection')[index];
						image.title = $("#title_button" + intId).val();
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
						else if(section === "prioritiesSlider"){
								files = that.prioritiesSliderFiles;
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

						that.handleFiles(data.files, data.fileInput);
					}
				},
				done: function(e, data) {
					/*
					 * After the file was submitted this function is called to set
					 * image attribute in the model and, then trigger save funciton
					 * if it is the last element in the table
					 *
					 **/

					var input = $("#" + data.fileInput[0].id);
						/* We replace the label for the img src, because we can now display img src due it is
						 *an external source
						 */

					if (window.FileReader === undefined) {
						input.parent().parent().find('label').remove()
						input.parent().parent().before("<img src=" + data.result['url'] + " alt=\"\"class=\"FL\"/>");
					}

					console.log(input);
					var inputRow = input.closest('tr');
					var inputUrl = inputRow.find("input[type=url]");
					var inputTitle = inputRow.find("input[name^='title']");
					var inputDescription = inputRow.find("input[name^='description']");
					var href = '';
					var title = '';
					var description = '';
					if (typeof inputUrl.val() != 'undefined') {
						href = inputUrl.val();
					}
					if (typeof inputTitle.val() != 'undefined') {
						title = inputTitle.val();
					}
					if (typeof inputDescription.val() != 'undefined') {
						description = inputDescription.val();
					}
					if (data.fileInput[0].id.indexOf("btn_file_image") >= 0) {
						that.model.get('buttonSection').splice(inputRow.index(), 1, {
							'image': data.result['url'],
							'href': href,
							'title': title,
							'description': description
						});
					} else if (data.fileInput[0].id.indexOf("file_image") >= 0){
						that.model.get('imageSliderSection').splice(inputRow.index(), 1, {
							'image': data.result['url'],
							'href': href,
							'title': title,
							'description': description
						});
					} else if (data.fileInput[0].id.indexOf("priorities_file") >= 0){
						that.model.get('prioritiesSliderSection').splice(inputRow.index(), 1, {
							'image': data.result['url'],
							'href': href,
							'title': title,
							'description': description
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
					var titleInput = $(this).find("input[type=text]");
					if (image != undefined && image.title != titleInput.val()) {
							image.title = titleInput.val();
					}
					var descriptionInput = $(this).find("input[type=text]");
					if (image != undefined && image.description != descriptionInput.val()) {
							image.description = descriptionInput.val();
					}
				});

			}
		});
	},

	initMiddleBottomImage : function () {
		var that = this;
		
		$('#id_middle_bottom_background_color').val(that.model.get('middleBottomSectionBackgroundColor'));

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
		
		$('#id_left_bottom_background_color').val(that.model.get('leftBottomSectionBackgroundColor'));

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
		
		$('#id_right_bottom_background_color').val(that.model.get('rightBottomSectionBackgroundColor'));

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

	initLinksSection : function () {
		var that = this;
		_.each(this.model.get('links'), function (item, index) {

			var intId = that.linksCont;
			var linkTextId = "link_text-" + intId;
			var linkUrlId = "link_url-" + intId;
			var buttonText = gettext('ADMIN-HOME-SECTION-BUTTONS-TEXT-LABEL');
			var linkText = gettext('ADMIN-HOME-SECTION-BUTTONS-LINK-LABEL');
			var placeholderText = gettext('ADMIN-HOME-SECTION-BUTTONS-TEXT-PLACEHOLDER');
			var placeholderLink = gettext('ADMIN-HOME-SECTION-BUTTONS-LINK-PLACEHOLDER');
			var deleteText = gettext('ADMIN-HOME-SECTION-DELETESLIDE');
			var row =
				'<tr class=\"template-upload fade\" id=\"row' + intId + '\">' +
				'<td class="draggableSection"><i class="arrangeIcon"></i></td>' +
				'<td>' +
				'<div class=\"clearfix\">' +
				'<div class=\"FL clearfix\">' +
				'<label for=\"' + linkTextId + '\" class=\"FL\">' + buttonText + '</label>' +
				'<input type=\"text\" id=\"' + linkTextId + '\" name =\"'+linkTextId+'\" value=\"' + item.linkText + '\" class=\"field FL requiredText \"  placeholder=\"' + placeholderText + '\"/>' +
				'<label for=\"' + linkUrlId + '\"class=\"FL\">' + linkText + '</label>' +
				'<div class=\"formErrorMessageContainer FL\">' +
				'<input type=\"url\" id=\"' + linkUrlId + '\" value=\"' + item.linkURL + '\" class=\"field FL urlLink complete_url requiredText\" placeholder=\"' + placeholderLink + '\"/>' +
				'</div>' +
				'</div>' +
				'<input type=\"button\" id=\"btn_' + intId + '\" class=\"remove FR\" value=\"' + deleteText + '\"/>' +
				'</div>' +
				'</td>' +
				'</tr>'

				$("#links_table").append(row);

			// We make the table sortable
			$("#links_table tbody").sortable({});

			that.linksCont += 1;
		});

	},

	addLinksInput : function () {
		var that = this;
		var last_links_row = $("#links_table tr:last");

		if (
			($("#links_table tr").length < 1) ||
			(
				($("#links_table tr").length >= 1) &&
				(typeof last_links_row) != 'undefined' &&
				(
					last_links_row.find("input[id^=link_text-]").val() != '' ||
					last_links_row.find("input[id^=link_url-]").val() != ''))) {

			var intId = that.linksCont;
			var linkTextId = "link_text-" + intId;
			var linkUrlId = "link_url-" + intId;
			that.linksCont += 1;
			var buttonText = gettext('ADMIN-HOME-SECTION-BUTTONS-TEXT-LABEL');
			var linkText = gettext('ADMIN-HOME-SECTION-BUTTONS-LINK-LABEL');
			var placeholderText = gettext('ADMIN-HOME-SECTION-BUTTONS-TEXT-PLACEHOLDER');
			var placeholderLink = gettext('ADMIN-HOME-SECTION-BUTTONS-LINK-PLACEHOLDER');
			var deleteText = gettext('ADMIN-HOME-SECTION-DELETESLIDE');
			var row =
				'<tr class=\"template-upload fade\" id=\"row' + intId + '\">' +
				'<td class="draggableSection"><i class="arrangeIcon"></i></td>' +
				'<td>' +
				'<div class=\"clearfix\">' +
				'<div class=\"FL clearfix\">' +
				'<label for=\"' + linkTextId + '\" class=\"FL\">' + buttonText + '</label>' +
				'<div class=\"formErrorMessageContainer FL\">' +
				'<input type=\"text\" id=\"' + linkTextId + '\" name =\"'+linkTextId+'\" class=\"field FL requiredText\" placeholder=\"' + placeholderText + '\"/>' +
				'</div>' +
				'<label for=\"' + linkUrlId + '\"class=\"FL\">' + linkText + '</label>' +
				'<div class=\"formErrorMessageContainer FL\">' +
				'<input type=\"url\" id=\"' + linkUrlId + '\" class=\"field FL urlLink complete_url requiredText\" placeholder=\"' + placeholderLink + '\"/>' +
				'</div>' +
				'</div>' +
				'<input type=\"button\" id=\"btn_' + intId + '\" class=\"remove FR\" value=\"' + deleteText + '\"/>' +
				'</div>' +
				'</td>' +
				'</tr>';

			$("#links_table").append(row);

			// We make the table sortable
			$("#links_table tbody").sortable({});

			// Add spacebar, enter and click to browse button, to trigger file upload
			this.setBrowseButtonTrigger(intId);

		} else {
			$('#links_table tbody tr:last-child').addClass('highlight');
			setTimeout("$('#links_table tbody tr:last-child').removeClass('highlight');", 2000);
		}

	},

	removeRow : function (event) {
		var button = event.currentTarget;
		$(button).parents("tr").remove();
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
				var labelField = $("#" + input).parent().parent().find('label');
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
			if (table.is(".featuredSection #image_saved")) {
				that.model.get('imageSliderSection').push("");
				var row = $("#" + input).closest("tr");
				row.detach();

				$(".featuredSection #image_table").append(row);
				var tdSort = '<td class=\"draggableSection\"><i class=\"arrangeIcon\"></i></td>'
				$('.featuredSection #image_table tr:last td:eq(0)').before(tdSort);
				this.setTableSortable($(".featuredSection #image_table"), that.model.get('imageSliderSection'));

			} else if (table.is(".prioritiesSection #image_saved")) {
				that.model.get('prioritiesSliderSection').push("");
				var row = $("#" + input).closest("tr");
				row.detach();

				$(".prioritiesSection #image_table").append(row);
				var tdSort = '<td class=\"draggableSection\"><i class=\"arrangeIcon\"></i></td>'
				$('.prioritiesSection #image_table tr:last td:eq(0)').before(tdSort);
				this.setTableSortable($(".prioritiesSection #image_table"), that.model.get('prioritiesSliderSection'));

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

	removeWelcomeImage : function () {
		if (this.model.get('welcomeSectionImageUrl') != undefined) {
			this.model.set('welcomeSectionImageUrl', undefined);
		}
		var deleteBtn = $("#id_btnRemoveWelcome")
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

				if (typeof that.welcomeImage != 'undefined' && that.welcomeImage != '') {
					ajaxReqs.push($("#id_welcomeImage").fileupload('send', {
							fileInput : that.welcomeImage.fileInput,
							files : that.welcomeImage.files
						}));
				}

				_.each(that.sliderFiles, function(item, index) {
					ajaxReqs.push($("#" + item['input'][0].id).fileupload('send', {
						fileInput: item['input'],
						files: item['file']
					}));
				})

				_.each(that.prioritiesSliderFiles, function(item, index) {
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

				if (that.sliderFiles.length > 0 || that.buttonFiles.length > 0 || that.prioritiesSliderFiles.length > 0) {
					//We loop through the request, once the all the ajax calls are done, we trigger the save preference
					$.when.apply($, ajaxReqs).then(function() {
						that.sliderFiles = [];
						that.prioritiesSliderFiles = [];
						that.buttonFiles = [];
						that.saveLinks(event);
						that.savePreference(event);
					})
				} else {
					$.when.apply($, ajaxReqs).then(function() {
						that.saveLinks(event);
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

	saveLinks : function (event) {
		console.log("save");
		//run through each row
		var links = [];
		$('#links_table tr').each(function (i, row) {
			var obj = {
				linkText : $(row).find("input[id^=link_text-]").val(),
				linkURL : $(row).find("input[id^=link_url-]").val()
			};
			links.push(obj)

		});
		that.model.set('links', links);
	},

	savePreference: function(event) {
		this.setColors();
		var btn_id = $(event.currentTarget).attr("id");
		var ob = {};
		if (btn_id === 'id_save') {
			this.options.currentModel.attributes.config = this.model.toJSON();
			this.options.currentModel.attributes.themeID = '7';
			ob['config'] = this.options.currentModel.attributes.config;
			ob['theme'] = this.options.currentModel.attributes.themeID;
			ob['type'] = 'save';
		} else {
			ob['config'] = this.model.toJSON();
			ob['theme'] = '7';
			ob['type'] = 'preview';
		}
		$.ajax({
			type: 'POST',
			data: {
				'jsonString': saferStringify(ob)
			},
			dataType: 'json',
			beforeSend: function() {
				$("#ajax_loading_overlay").show();
			},
			success: function(response) {
				$("#ajax_loading_overlay").hide();
				if (btn_id === "id_save") {
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

	colorPicker: function() {

		var that = this;

	    $('input[type=hidden][name*=_color]').each(function(){
	        var divId = $(this).attr('name');
	        var divBGColor = $(this).val();
	        $('#'+divId+' div').css('background-color', 'rgba(' + divBGColor + ',1)');
	    });

	    $('.colorPicker').ColorPicker({
        
	        onBeforeShow: function() {
	            var bg_color = $(this).children(0).css('background-color');
	            if (bg_color != null) {
	                $(this).ColorPickerSetColor(bg_color);
	            }
	        },
	        onShow: function (colpkr) {
	            $(colpkr).fadeIn(500);
	            return false;
	        },
	        onHide: function (colpkr) {
	            $(colpkr).fadeOut(500);
	            return false;
	        },
	        onChange: function (hsb, hex, rgb) {
	            element = $(this).data('colorpicker').el
	            $(element).find('div').css('background-color', 'rgba(' + rgb.r + ',' + rgb.g + ',' + rgb.b + ',1)');
	            var elementId = $(element).attr('id');
	            $('input[name='+elementId+']').val( rgb.r + ',' + rgb.g + ',' + rgb.b );
	        }

	    });
	},

	setColors: function(){
	    var color = {};

	    color.welcome_background_color = $('#id_welcome_background_color').val();
	    color.featured_background_color = $('#id_featured_background_color').val();
	    color.priorities_background_color = $('#id_priorities_background_color').val();
	    color.buttons_background_color = $('#id_buttons_background_color').val();
	    color.left_bottom_background_color = $('#id_left_bottom_background_color').val();
	    color.middle_bottom_background_color = $('#id_middle_bottom_background_color').val();
	    color.right_bottom_background_color = $('#id_right_bottom_background_color').val();

		this.model.set('welcomeSectionBackgroundColor', color.welcome_background_color);
		this.model.set('featuredSliderSectionBackgroundColor', color.featured_background_color);
		this.model.set('prioritiesSliderSectionBackgroundColor', color.priorities_background_color);
		this.model.set('buttonSectionBackgroundColor', color.buttons_background_color);
		this.model.set('leftBottomSectionBackgroundColor', color.left_bottom_background_color);
		this.model.set('middleBottomSectionBackgroundColor', color.middle_bottom_background_color);
		this.model.set('rightBottomSectionBackgroundColor', color.right_bottom_background_color);

		console.log(color);	    
	    return color;

	}

});