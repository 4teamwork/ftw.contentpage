import logging

logger = logging.getLogger('PloneFlashUpload')
logger.level = logging.getLogger().level

from Acquisition import aq_inner, aq_parent, aq_base
from collective.quickupload.interfaces import IQuickUploadCapable
from collective.quickupload.interfaces import IQuickUploadNotCapable
from Products.Archetypes.utils import shasattr
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.FactoryTool import TempFolder
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class FlashUploadForm(BrowserView):
    """IE drives me cracy. We have to load the form contents with ajax, because
    of this --> https://dev.plone.org/plone/ticket/10894
    Otherwise it will no work with IE < 9.
    IMPORTANT: If this view will not work in the future, consider the JAVASCRIPT
    variable of the quickuploadportlet.py"""

    template = ViewPageTemplateFile('flashupload.pt')

    def __call__(self):
        return self.template()


    def get_upload_url(self):
        """
        return upload url
        in current folder
        """
        ploneview = self.context.restrictedTraverse('@@plone')
        folder_url = ploneview.getCurrentFolderUrl()
        return '%s/@@quick_upload' %folder_url


    def javascript(self):
        return """
  if (jQuery.browser.msie) jQuery("#settings").remove();
  var Browser = {};
  Browser.onUploadComplete = function() {
      window.location.reload();
  }
  loadUploader = function() {
      var ulContainer = jQuery('.quickupload.uploaderContainer');
      ulContainer.each(function(){
          var uploadUrl =  jQuery('.uploadUrl', this).val();
          var uploadData =  'auto';
          var UlDiv = jQuery(this);
          jQuery.ajax({
                     type: 'GET',
                     url: uploadUrl,
                     data: uploadData,
                     dataType: 'html',
                     contentType: 'text/html; charset=utf-8',
                     success: function(html) {
                        if (html.indexOf('quick-uploader') != -1) {
                            UlDiv.html(html);
                        }
                     } });
      });
  }
  jQuery(document).ready(loadUploader);
"""



def isTemporary(obj):
    """Check to see if an object is temporary"""
    if not shasattr(obj, 'isTemporary'):
        return False
    if obj.isTemporary():
        return False

    parent = aq_base(aq_parent(aq_inner(obj)))
    return hasattr(parent, 'meta_type') \
        and parent.meta_type == TempFolder.meta_type


class DisplayUploadView(BrowserView):

    def can_upload(self):

        context = aq_inner(self.context)
        mtool = getToolByName(self.context, 'portal_membership')

        if not IQuickUploadCapable.providedBy(context):
            return False
        elif IQuickUploadNotCapable.providedBy(context):
            return False
        elif not mtool.checkPermission('Add portal content', context):
            return False
        elif isTemporary(context):
            return False

        upload_portal_type = 'auto'
        if (upload_portal_type and upload_portal_type != 'auto'
                and upload_portal_type not in [t.id for t
                        in self.context.getAllowedTypes()]):
            return False
        else:
            return True
