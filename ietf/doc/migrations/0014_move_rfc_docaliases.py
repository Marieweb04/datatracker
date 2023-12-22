# Generated by Django 4.2.2 on 2023-06-20 18:36

from django.db import migrations


def forward(apps, schema_editor):
    """Point "rfc..." DocAliases at the rfc-type Document

    Creates a became_rfc RelatedDocument to preserve the connection between the draft and the rfc.
    """
    DocAlias = apps.get_model("doc", "DocAlias")
    Document = apps.get_model("doc", "Document")
    RelatedDocument = apps.get_model("doc", "RelatedDocument")

    for rfc_alias in DocAlias.objects.filter(name__startswith="rfc"):
        rfc = Document.objects.get(name=rfc_alias.name)
        aliased_doc = rfc_alias.docs.get()  # implicitly confirms only one value in rfc_alias.docs
        if aliased_doc != rfc:
            # If the DocAlias was not already pointing at the rfc, it was pointing at the draft
            # it came from. Create the relationship between draft and rfc Documents.
            assert aliased_doc.type_id == "draft", f"Alias for {rfc.name} should be pointing at a draft"
            RelatedDocument.objects.create(
                source=aliased_doc,
                target=rfc_alias,
                relationship_id="became_rfc",
            )
            # Now move the alias from the draft to the rfc 
            rfc_alias.docs.set([rfc])


class Migration(migrations.Migration):
    dependencies = [
        ("doc", "0013_rfc_relateddocuments"),
    ]

    operations = [
        migrations.RunPython(forward),
    ]
