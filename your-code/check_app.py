"""Check your app without a browser. Run it from the your-code folder:

    python check_app.py

Each line says what the page showed, so you can compare it with the checkpoints in the README.
"""

from streamlit.testing.v1 import AppTest


def run(path, timeout=120):
    at = AppTest.from_file(path, default_timeout=timeout).run()
    if at.exception:
        print(f"{path}: ERROR {at.exception[0].message}")
    return at


at = run("Home.py")
print("Home:", "title OK" if at.title else "no title", "|", "image OK" if at.get("image") else "no image",
      "| metrics:", [(m.label, m.value) for m in at.metric])

at = run("pages/1_Explore.py")
charts = [chart.proto.spec for chart in at.get("vega_lite_chart")]
print("Explore:", sum('"line"' in spec for spec in charts), "line chart(s),", sum('"bar"' in spec for spec in charts),
      "bar chart(s),", len(at.dataframe), "table(s)")
for table in at.dataframe:
    print("   ", table.value.head(5).to_dict("records"))

at = run("pages/2_Find_similar_films.py")
if at.text_area and at.button:
    at.text_area[0].input("A thoughtful drama about a monk who discovers a shark in Australia").run()
    at.button[0].click().run()
    print("Similar films:", [m.value for m in at.markdown if "similarity" in m.value.lower()][:3] or "no results shown")
else:
    print("Similar films: no text area or button yet")
