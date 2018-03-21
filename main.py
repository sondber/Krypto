import data_import_support as dis
from Sondre import sondre_support_formulas as sup
from Sondre.sondre_support_formulas import unix_to_timestamp

exc_name="krakeneur"
start_stamp=unix_to_timestamp(1389173189)
end_stamp=unix_to_timestamp(1514764800)

dis.import_from_csv_w_ticks(exc_name, start_stamp, end_stamp)