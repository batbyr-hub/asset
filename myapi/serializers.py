from rest_framework import serializers

from .models import AssetPackageData

class DataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AssetPackageData
        fields = ('id', 'assetslipid', 'assetgroupname', 'assetname', 'assetbarcode', 'locationfrom', 'locationto','createddate', 'location_id', 'locationfrom_id', 'userfrom', 'userto', 'gazar', 'returnis', 'reasonvalue', 'uploadfile', 'lenghtcable', 'status')