import pandas as pd
from styleframe import StyleFrame

df = pd.DataFrame(
    [
        ["First Line\nSecond line"],
        ["First line\nsecond line\nthird line"],
        ["first line"],
    ]
)

# StyleFrame(df).to_excel("test.xlsx")._save()


with pd.ExcelWriter("file.xlsx", engine="xlsxwriter") as writer:
    writer.book.formats[0].set_text_wrap()  # update global format with text wrap
    df.to_excel(writer, sheet_name="Sheet1", index=False, header=False)
    df.to_excel(writer, sheet_name="Sheet2", index=False, header=False)
