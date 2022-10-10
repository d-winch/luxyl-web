from django.core.files import storage
from django.db import models
from os.path import dirname, join
import csv
from django.core.files.storage import FileSystemStorage


class Design(models.Model):
    
    #fs = FileSystemStorage(location='/designs/pngs')
    design_code = models.CharField(max_length=20, primary_key=True)
    title = models.CharField(max_length=250)
    png = models.ImageField(upload_to='designs/pngs')

    class Meta:
        verbose_name = ("Design")
        verbose_name_plural = ("Designs")

    def __str__(self):
        return self.design_code

    def import_from_csv(self, csv_filename):
        designs = []
        with open(csv_filename, newline='') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in csv_reader:
                designs.append(row)
        for design in designs:
            ship, created = Design.objects.update_or_create(
                design_code=design[0],
                defaults={
                    'title': design[1],
                    'png': f"designs/pngs/{design[2]}",
                },
            )