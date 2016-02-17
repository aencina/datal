var theme5View = Backbone.Epoxy.View.extend({
		el : '#id_themeForm',
		template : null,
		welcomeImage : "",
		featuredImage : "",
		middleBottomImage : "",
		leftBottomImage : "",
		rightBottomImage : "",
		linksCont : 0,
		buttonsCont : 0,

		events : {
			"click #id_new_slide" : "addLinksInput",
			"click #id_new_button" : "addButtonsInput",
			"click #id_btnRemoveWelcome" : "removeWelcomeImage",
			"click #id_btnRemoveFeatured" : "removeFeaturedImage",
			"click #id_btnRemoveLeftBottom" : "removeLeftBottomImage",
			"click #id_btnRemoveMiddleBottom" : "removeMiddleBottomImage",
			"click #id_btnRemoveRightBottom" : "removeRightBottomImage",
			"click #links_section tr .remove, #buttons_table tr .remove" : "removeRow"
		},

		initialize : function (options) {
			this.currentView = options.currentView;
			this.currentModel = options.currentModel;

			this.currentView.helpAndTips('show');
			this.template = _.template($("#id_theme5Template").html());
			this.render();
			this.initWelcomeImage();
			this.initFeaturedImage();
			this.initMiddleBottomImage();
			this.initLeftBottomImage();
			this.initRightBottomImage();
			this.initButtonsSection();
			this.initLinksSection();
		},

		render : function () {

			this.$el.html(this.template(this.model.attributes));
			return this;
		},

		configColorPicker : function (element) {
			var self = this;
			element.find('.colorPicker').ColorPicker({
				onBeforeShow: function() {
          var bg_color = self.rgbToHex($(this).children(0).css('background-color'));
          if (bg_color != null) {
              $(this).ColorPickerSetColor(bg_color);
          }
        },
				onShow : function (colpkr) {
					$(colpkr).fadeIn(500);
					return false;
				},
				onHide : function (colpkr) {
					$(colpkr).fadeOut(500);
					return false;
				},
				onChange : function (hsb, hex, rgb) {
					element = $(this).data('colorpicker').el;
					$(element).find('div').css('background-color', '#' + hex);
					$(element).parent().find('input[id^=button_colorHex-]').val(hex);
				}
			});

		},

		rgbToHex: function(rgb) {
      var rgbvals = /rgb\((.+),(.+),(.+)\)/i.exec(rgb);
      if (rgbvals == null) {
          return null;
      }
      var rval = parseInt(rgbvals[1]);
      var gval = parseInt(rgbvals[2]);
      var bval = parseInt(rgbvals[3]);
      return '#' + ( 
        rval.toString(16) +
        gval.toString(16) +
        bval.toString(16)
      ).toUpperCase();
    },

		initButtonsSection : function () {
			var that = this;
			var html = '';

			_.each(this.model.get('buttonSection'), function (item, index) {

				var intId = that.buttonsCont;
				var buttonTextId = "button_text-" + intId;
				var buttonUrlId = "button_url-" + intId;
				var buttonColorHexId = "button_colorHex-" + intId;
				var buttonColorId = "button_color-" + intId;
				var buttonDeleteId = "button_delete-" + intId;
				var last_buttons_row = $("#buttons_table tr:last");
				var button_label_text = gettext('ADMIN-HOME-SECTION-BUTTONS-TEXT-LABEL');
				var button_label_link = gettext('ADMIN-HOME-SECTION-BUTTONS-LINK-LABEL');
				var button_placeholder_text = gettext('ADMIN-HOME-SECTION-BUTTONS-TEXT-PLACEHOLDER');
				var button_placeholder_link = gettext('ADMIN-HOME-SECTION-BUTTONS-LINK-PLACEHOLDER');
				var button_label_background = gettext('ADMIN-HOME-SECTION-BUTTONS-BACKGROUND-LABEL');
				var delete_text = gettext('ADMIN-HOME-SECTION-DELETE');

				var row =
					'<tr class=\"template-upload fade\" id=\"row' + intId + '\">' +
					'<td class=\"draggableSection"><i class="arrangeIcon"></i></td>' +
					'<td>' +
					'<div class=\"clearfix\">' +
					'<label for=\"' + buttonTextId + '\" class=\"FL\">' + button_label_text + '</label>' +
					'<div class=\"formErrorMessageContainer FL\">' +
					'<input type=\"text\" id=\"' + buttonTextId + '\" name=\"'+ buttonTextId +'\" value=\"' + item.btnText + '\" class=\"field FL requiredText\" placeholder=\"' + button_placeholder_text + '\"/>' +
					'</div>' +
					'<label for=\"' + buttonUrlId + '\" class=\"FL\">' + button_label_link + '</label>' +
					'<div class=\"formErrorMessageContainer FL\">' +
					'<input type=\"url\" id=\"' + buttonUrlId + '\" value=\"' + item.btnURL + '\" class=\"field FL urlLink complete_url requiredText\" placeholder=\"' + button_placeholder_link + '\"/>' +
					'</div>' +
					'<label for=\"' + buttonColorId + '\" class=\"FL\">' + button_label_background + '</label>' +
					'<div id=\"' + buttonColorId + '\" class=\"colorPicker\">' +
					'<div style=\"background-color:' + item.btnHexColor + ';\"></div>' +
					'<input type=\"hidden\" id=\"' + buttonColorHexId + '\" value=\"' + item.btnHexColor.split('#')[1] + '\"/>' +
					'</div>' +
					'<input type=\"button\" id=\"' + buttonDeleteId + '\" class=\"remove FR\" value=\"' + delete_text + '\"/>' +
					'</div>' +
					'</td>' +
					'</tr>';

				html += row;

				that.buttonsCont += 1;

			});

			$("#buttons_table").append(html);

			// Set all Color pickers
			that.configColorPicker($("#buttons_table"));

			// Make the table sortable
			$("#buttons_table tbody").sortable({});

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

		removeRow : function (event) {
			var button = event.currentTarget;
			$(button).parents("tr").remove();
		},

		initWelcomeImage : function () {
			var that = this;

			var welcomeImageUrl = that.model.attributes.welcomeImageUrl;

			if (typeof welcomeImageUrl != 'undefined' && welcomeImageUrl != '') {
				var img = $('<img>');
				img.attr('src', welcomeImageUrl);
				$("#id_welcomeImage").parent().before(img);
				$("#id_btnRemoveWelcome").show();
			}

			// Add spacebar, enter and click to browse button, to trigger file upload
			that.setBrowseButtonTrigger();

			$('#id_welcomeImage').fileupload({
				url : '/personalizeHome/upload/',
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

					that.model.set('welcomeImageUrl', data.result['url']);

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

		initFeaturedImage : function () {
			var that = this;

			var featuredImageUrl = that.model.attributes.featuredImageUrl;

			if (typeof featuredImageUrl != 'undefined' && featuredImageUrl != '') {
				var img = $('<img>');
				img.attr('src', featuredImageUrl);
				$("#id_featuredImage").parent().before(img);
				$("#id_btnRemoveFeatured").show();
			}

			// Add spacebar, enter and click to browse button, to trigger file upload
			that.setBrowseButtonTrigger();

			$('#id_featuredImage').fileupload({
				url : '/personalizeHome/upload/',
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
						that.featuredImage = data
							var fileInput = {
							inputElement : this,
							inputFiles : data.files,
							inputRemove : $("#id_btnRemoveFeatured")
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
						$("#id_featuredImage").parent().parent().find('label').remove()
						$("#id_feturedImage").parent().before("<img src=" + data.result['url'] + " alt=\"\"class=\"FL\"/>");
					}

					that.model.set('featuredImageUrl', data.result['url']);

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
				url : '/personalizeHome/upload/',
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
				url : '/personalizeHome/upload/',
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
				url : '/personalizeHome/upload/',
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

		addButtonsInput : function () {
			var that = this;

			var intId = that.buttonsCont;
			var buttonTextId = "button_text-" + intId;
			var buttonUrlId = "button_url-" + intId;
			var buttonColorHexId = "button_colorHex-" + intId;
			var buttonColorId = "button_color-" + intId;
			var buttonDeleteId = "button_delete-" + intId;
			that.linksCont += 1;
			var last_buttons_row = $("#buttons_table tr:last");
			var button_label_text = gettext('ADMIN-HOME-SECTION-BUTTONS-TEXT-LABEL');
			var button_label_link = gettext('ADMIN-HOME-SECTION-BUTTONS-LINK-LABEL');
			var button_placeholder_text = gettext('ADMIN-HOME-SECTION-BUTTONS-TEXT-PLACEHOLDER');
			var button_placeholder_link = gettext('ADMIN-HOME-SECTION-BUTTONS-LINK-PLACEHOLDER');
			var button_label_background = gettext('ADMIN-HOME-SECTION-BUTTONS-BACKGROUND-LABEL');
			var delete_text = gettext('ADMIN-HOME-SECTION-DELETE');

			if (
				($("#buttons_table tr").length < 1) ||
				(
					($("#buttons_table tr").length >= 1) &&
					(typeof last_buttons_row) != 'undefined' &&
					(
						last_buttons_row.find("input[id^=button_text-]").val() != '' ||
						last_buttons_row.find("input[id^=button_url-]").val() != ''))) {

				var row =
					'<tr class=\"template-upload fade\" id=\"row' + intId + '\">' +
					'<td class=\"draggableSection"><i class="arrangeIcon"></i></td>' +
					'<td>' +
					'<div class=\"clearfix\">' +
					'<label for=\"' + buttonTextId + '\" class=\"FL\">' + button_label_text + '</label>' +
					'<div class=\"formErrorMessageContainer FL\">' +
					'<input type=\"text\" id=\"'+ buttonTextId +'\" name=\"'+ buttonTextId +'\" class=\"field FL requiredText\" placeholder=\"' + button_placeholder_text + '\"/>' +
					'</div>' +
					'<label for=\"' + buttonUrlId + '\" class=\"FL\">' + button_label_link + '</label>' +
					'<div class=\"formErrorMessageContainer FL\">' +
					'<input type=\"url\" id=\"' + buttonUrlId + '\" class=\"field FL urlLink complete_url requiredText\" placeholder=\"' + button_placeholder_link + '\"/>' +
					'</div>' +
					'<label for=\"' + buttonColorId + '\" class=\"FL\">' + button_label_background + '</label>' +
					'<div id=\"' + buttonColorId + '\" class=\"colorPicker\">' +
					'<div style=\"background-color:#666;\"></div>' +
					'<input type=\"hidden\" id=\"' + buttonColorHexId + '\" value=\"666\">' +
					'</div>' +
					'<input type=\"button\" id=\"' + buttonDeleteId + '\" class=\"remove FR\" value=\"' + delete_text + '\"/>' +
					'</div>' +
					'</td>' +
					'</tr>';

				$("#buttons_table").append(row);

				// We make the table sortable
				$("#buttons_table tbody").sortable({});

				// Add spacebar, enter and click to browse button, to trigger file upload
				this.setBrowseButtonTrigger(intId);

				that.configColorPicker($("#buttons_table tr:last"));

			} else {

				$('#buttons_table tbody tr:last-child').addClass('highlight');
				setTimeout("$('#buttons_table tbody tr:last-child').removeClass('highlight');", 2000);

			}

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

		removeWelcomeImage : function () {
			if (this.model.get('welcomeImageUrl') != undefined) {
				this.model.set('welcomeImageUrl', undefined);
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

		removeFeaturedImage : function () {
			if (this.model.get('featuredImageUrl') != undefined) {
				this.model.set('featuredImageUrl', undefined);
			}
			var deleteBtn = $("#id_btnRemoveFeatured")
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

		validateUrl : function () {

			$('.complete_url').validate({
				rules : {
					complete_url : true
				}
			});

		},
		save : function (event) {
			that = this;

			// set validate URL
			this.validateUrl();
			this.calculateButtonRowWidth();
                            // set up a rule for the class
			$.validator.addClassRules("requiredText", {
				required : true,
				minlength: 1
			});

			this.$el.parent().validate({

				rules : {
					id_buttonsPerRow : {
						number : true
					}
				},

				invalidHandler : function (event, validator) {
					
                                            var i = 0;
					for (i=0; i< validator.invalidElements().length; i++) {
					         //If the name is id_buttonsPerRow, then we display error message for non numeric
						if ($(validator.invalidElements()[i]).attr('name') == 'id_buttonsPerRow') {
							$.gritter.add({
								title : gettext('ADMIN-HOME-SECTION-NOTVALIDURL-TITLE'),
								text : gettext('ADMIN-HOME-SECTION-NOTVALIDNUM-TEXT'),
								image : '/static/workspace/images/common/ic_validationError32.png',
								sticky : false,
								time : 5000
							});
						} else {

							$.gritter.add({
								title : gettext('ADMIN-HOME-SECTION-ERROR-TITLE'),
								text : gettext('ADMIN-HOME-SECTION-EMPTY-TEXT'),
								image : '/static/workspace/images/common/ic_validationError32.png',
								sticky : false,
								time : 5000
							});
						}

					}

				}

			});
			

			if ($(".complete_url").valid() && this.$el.parent().valid()) {
				var ajaxReqs = [];

				if (typeof that.welcomeImage != 'undefined' && that.welcomeImage != '') {
					ajaxReqs.push($("#id_welcomeImage").fileupload('send', {
							fileInput : that.welcomeImage.fileInput,
							files : that.welcomeImage.files
						}));
				}

				if (typeof that.featuredImage != 'undefined' && that.featuredImage != '') {
					ajaxReqs.push($("#id_featuredImage").fileupload('send', {
							fileInput : that.featuredImage.fileInput,
							files : that.featuredImage.files
						}));
				}

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

				//We loop through the request, once the all the ajax calls are done, we trigger the save preference
				$.when.apply($, ajaxReqs).then(function () {
					that.saveLinks(event);
					that.saveButtons(event);
					that.savePreference(event);
				});

			} else {		
			
			if($(".complete_url").valid()!=1){
			    		
					$.gritter.add({
						title : gettext('ADMIN-HOME-SECTION-NOTVALIDURL-TITLE'),
						text : gettext('ADMIN-HOME-SECTION-NOTVALIDURL-TEXT'),
						image : '/static/workspace/images/common/ic_validationError32.png',
						sticky : false,
						time : 5000
					});
			}	

			}

		},

		saveButtons : function (event) {
			//run through each row
			var buttonSection = [];
			$('#buttons_table tr').each(function (i, row) {
				var obj = {
					btnText : $(row).find("input[id^=button_text-]").val(),
					btnURL : $(row).find("input[id^=button_url-]").val(),
					btnHexColor : '#' + $(row).find("input[id^=button_colorHex-]").val()
				};
				buttonSection.push(obj);
			});
			that.model.set('buttonSection', buttonSection);
		},

		saveLinks : function (event) {
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

		savePreference : function (event) {
			var btn_id = $(event.currentTarget).attr("id");
			var ob = {};
			if (btn_id === 'id_save' || btn_id === 'id_save_top') {
				this.currentModel.attributes.config = this.model.toJSON();
				this.currentModel.attributes.themeID = '5';
				ob['config'] = this.currentModel.attributes.config;
				ob['theme'] = this.currentModel.attributes.themeID;
				ob['type'] = 'save';
			} else {
				ob['config'] = this.model.toJSON();
				ob['theme'] = '5';
				ob['type'] = 'preview';
			}
			$.ajax({
				type : 'POST',
				data : {
					'jsonString' : saferStringify(ob)
				},
				dataType : 'json',
				beforeSend : function (xhr, settings) {

					// call global beforeSend func
					$.ajaxSettings.beforeSend(xhr, settings);
					
					$("#ajax_loading_overlay").show();
				},
				success : function (response) {
					$("#ajax_loading_overlay").hide();
					if (btn_id === "id_save" || btn_id === 'id_save_top') {
						$.gritter.add({
							title : gettext('ADMIN-HOME-SECTION-SUCCESS-TITLE'),
							text : gettext('ADMIN-HOME-SECTION-SUCCESS-TEXT'),
							image : '/static/workspace/images/common/ic_validationOk32.png',
							sticky : false,
							time : 3500
						});
					} else {
						event.preventDefault();
						var preview_home = response['preview_home']
							window.open(preview_home, '', 'width=1024,height=500,resizable=yes,scrollbars=yes');
					}
				},
				error : function (response) {
					$("#ajax_loading_overlay").hide();
					$.gritter.add({
						title : gettext('ADMIN-HOME-SECTION-ERROR-TITLE'),
						text : gettext('ADMIN-HOME-SECTION-ERROR-TEXT'),
						image : '/static/workspace/images/common/ic_validationError32.png',
						sticky : true,
						time : ''
					});
				},
				url : '/personalizeHome/save/'
			});

		},

		setBrowseButtonTrigger : function () {

			$('.imageComponent .crop button').off("keypress").on("keypress", function (e) {
				if (e.which == 32 || e.which == 13) { // spacebar or enter
					e.preventDefault();
					$(this).parent().find('input[type=file]').trigger("click");
				}
			}).on("click", function (e) {
				e.preventDefault();

				// Esto triggerea un comportamiento erroneo en todos los campos input. Les hace abrir una ventana de subir archivo.
				//$(this).parent().find('input[type=file]').trigger("click");
				
			});

		},

		calculateButtonRowWidth : function () {
			var that = this;

			var btnsPerRow = $("#id_buttonsPerRow").val();

			// If no value is set, the default value (20) will be set as row width
			if (btnsPerRow) {
				that.model.set('buttonsPerRowWidth', (100 / btnsPerRow).toString() );
			}			



		}

	});
