from rest_framework import serializers
import requests

from .models import PackageRelease, Project
from .pypi import version_exists, latest_version


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageRelease
        fields = ["name", "version"]
        extra_kwargs = {"version": {"required": False}}

    def validate(self, data):
        version = data["version"] if "version" in data else latest_version(data["name"])
        if(version is not None and version_exists(data["name"], version)):
            return { "name": data["name"], "version": version }
        raise serializers.ValidationError()
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["name", "packages"]

    packages = PackageSerializer(many=True)

    def validate(self, data):
        grouped_packages = {}
        for package in data["packages"]:
            if package["name"] in grouped_packages.keys():
                raise serializers.ValidationError()
            else:
                grouped_packages[package["name"]] = True
        return data

    def create(self, validated_data):
        print("criando projeto...")
        project = Project.objects.create(name = validated_data["name"])
        packages = validated_data["packages"]
        for package in packages:
            PackageRelease.objects.create(**package,project=project)
        print("projeto criado...", project)
        return project
