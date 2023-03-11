import pandas as pd
import json
import os
from datetime import datetime

fecha_actual = datetime.now().strftime("%d.%m.%Y")

dir_path = os.path.dirname(os.path.abspath(__file__))

doc_file = os.path.join(dir_path, "Carga_Masiva_CHI_para_editar.xlsx")
pas_file = os.path.join(dir_path, "2010000 PASIVO TRANSITORIO 27 12 2022.xlsx")
prov_file = os.path.join(dir_path, "Proovedores.xlsx")
json_file = os.path.join(dir_path, "json.json")
json_file2 = os.path.join(dir_path, "json_2.json")

list_debito = ["E3", "E2", "E1", "KA", "E6", "E4", "KS"]

with open(json_file) as json_file:
    json_dict = json.load(json_file)

with open(json_file2) as json_file2:
    json_dict2 = json.load(json_file2)


def read_xlsx(file, skip, sheet):
    df = pd.read_excel(file, skiprows=skip, sheet_name=sheet)
    df = json.loads(df.to_json(orient="records"))
    return df


# Endpoint DataReader


def add_fields(xlsx_file, json_data, rows, sheet, pos, column_to_compare, column_to_find):
    final_data = ""
    data = []
    excel_df = pd.DataFrame(read_xlsx(xlsx_file, rows, sheet))
    excel_df[column_to_compare] = excel_df[column_to_compare].astype(str)
    result = []
    for i in range(0, excel_df.shape[0]):
        try:
            value = str(
                excel_df.loc[
                    excel_df[column_to_compare] == (json_data[pos]["value"]), column_to_find
                ].values[i]
            )
            if value == "None":
                value = ""
            data.append(value)
        except Exception:
            break
    if len(data) != 0:
        final_data = ";".join(data)
    new_value = {"name": column_to_find, "value": final_data, "valid": True}
    result.append(new_value)
    return result


# Fin Endpoint

list_of_data = [
    [pas_file, 3, 0, 11, "Doc.compr.", " Pos."],
    [pas_file, 3, 0, 11, "Doc.compr.", "Extrae Año GR"],
    [pas_file, 3, 0, 11, "Doc.compr.", "Extrae Entrega GR"],
    [prov_file, 4, 0, 1, "RUT / CUIT", "Acreedor/Vendor"],
    [doc_file, 2, 2, 1, "CUIT", "Vías pago Alimentos"],
    [doc_file, 2, 2, 1, "CUIT", "Vías pago Bebidas"],
    [doc_file, 0, 3, 10, "CUIT", "CODIGO SAP"],
    [doc_file, 0, 4, 9, "Código", "Codigo SAP"],
]


def format_montos(string):
    string_list = list(string)
    string_list.insert(-2, ",")
    string = "".join(string_list)
    return string


df_final = pd.DataFrame()
json_list = [json_dict, json_dict2]  # Param del Endpoint
for dic in json_list:
    result_complete = []
    if dic[0]["valid"]:
        # Param del Endpoint
        for data in list_of_data:
            response = add_fields(data[0], dic, data[1], data[2], data[3], data[4], data[5])
            result_complete.extend(response)

    dic.extend(result_complete)
    df_temp = pd.DataFrame.from_records(dic)
    df_temp = df_temp.drop(columns=["valid"])
    df_temp = df_temp.set_index("name").T
    df_temp["mnttotal"][0] = format_montos(df_temp["mnttotal"][0])
    df_temp["mnt"][0] = format_montos(df_temp["mnt"][0])

    df_temp["Moneda"] = "CLP"
    df_temp["Texto De Cabecera"] = fecha_actual
    df_temp["Via de pago"] = df_temp["Vías pago Alimentos"].astype(str) + df_temp[
        "Vías pago Bebidas"
    ].astype(str)
    if df_temp["Codigo SAP"].isin(list_debito).any():
        df_temp["Indicador Debito o Credito"] = "S"
    else:
        df_temp["Indicador Debito o Credito"] = "H"

    if df_temp["mntexe"] is not None:
        df_temp["Indicador de Impuesto"] = "CA"
    elif df_temp["iva"] is not None:
        df_temp["Indicador de Impuesto"] = "CB"
    elif df_temp["montoimp"] is not None:
        df_temp["Indicador de Impuesto"] = "CH"
    else:
        df_temp["Indicador de Impuesto"] = None

    df_temp.insert(
        len(df_temp.columns), "Posicion de la Nota De Entrega", df_temp[" Pos."].str.split(";")
    )
    df_temp.insert(len(df_temp.columns), "GR Año Fiscal", df_temp["Extrae Año GR"].str.split(";"))
    df_temp.insert(
        len(df_temp.columns), "Nota de Entrega GR", df_temp["Extrae Entrega GR"].str.split(";")
    )
    df_temp = df_temp.explode(
        ["Posicion de la Nota De Entrega", "GR Año Fiscal", "Nota de Entrega GR"]
    )

    cols = df_temp.columns[:-3]
    for col in cols:
        for i in range(1, df_temp.shape[0]):
            if (
                df_temp.iloc[i, df_temp.columns.get_loc(col)]
                == df_temp.iloc[0, df_temp.columns.get_loc(col)]
            ):
                df_temp.iloc[i, df_temp.columns.get_loc(col)] = None

    df_final = pd.concat([df_final, df_temp], ignore_index=True)

df_final["fchemis"] = pd.to_datetime(df_final["fchemis"], format="%Y-%m-%d")
df_final["fchemis"] = df_final["fchemis"].dt.strftime("%d.%m.%Y")
df_final["fchemis_1"] = df_final["fchemis"]
df_final.rename(
    columns={
        "folio": "Referencia",
        "Acreedor/Vendor": "Numero Acreedor",
        "CODIGO SAP": "Sociedad",
        "Codigo SAP": "Clase Documento",
        "fchemis": "Fecha Factura",
        "rznsoc": "Nombre del Proovedor",
        "fchemis_1": "Fecha Base",
        "mnttotal": "Importe Factura",
        "folioref": "OC",
        "mnt": "Importe Gasto",
    },
    inplace=True,
)
df_final = df_final.reindex(
    columns=[
        "Referencia",
        "Numero Acreedor",
        "Sociedad",
        "Clase Documento",
        "Fecha Factura",
        "Moneda",
        "Tipo de Cambio",
        "Nombre del Proovedor",
        "Fecha Base",
        "Texto De Cabecera",
        "Importe Factura",
        "Bloqueo Factura",
        "Columna M-O",
        "Via de pago",
        "OC",
        "Nota de Entrega GR",
        "GR Año Fiscal",
        "Posicion de la Nota De Entrega",
        "Cuenta",
        "Importe Gasto",
        "Indicador Debito o Credito",
        "Columna X-Z",
        "Indicador de Impuesto",
        "Columna AB-AY",
        "Valid",
    ]
)  # Esto definirlo en otro lado

df_final.to_excel(f"{dir_path}\\output_2.xlsx", index=False)
print("Excel generado")

pass
