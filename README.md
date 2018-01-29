pyscrapper_leboncoin
====================

Une api python pour parser les annoces le bonc coin.
Pour le moment uniquement utilisable pour l'immobilier.


# arguments
## obligatoires
type_bien (string) : type de bien (maison, appartement, terrain)

## optionnelles
-h, --help : show the help message and exit
--nbr_piece (int) : nombre de pièce minimale (default = 0)
--prix_max : prix maximal (default = 0)
--surface_min (int) : surface minimale (default = 0)
--image (bool) : display images in report (default = False)
--report_name (string) : nom du rapport (default = report.pdf)

