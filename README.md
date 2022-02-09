<h1 align="center">
 Graph Technology Landscape 2022
</h1>

This repository holds data about popular graph technologies in 2022. It imports them into Memgraph and creates cool visualization in Memgraph Lab.

## Memgraph Lab Styling

```
@NodeStyle {
size: 50
border-width: 5
border-color: #ffffff
shadow-color: #bab8bb
shadow-size: 6
}

@NodeStyle Greater?(Size(Labels(node)), 0) {
label: Format(":{}", Join(Labels(node), " :"))
}

@NodeStyle HasLabel?(node, "Company") {
color: #dd2222
color-hover: Darker(#dd2222)
color-selected: #dd2222
}

@NodeStyle HasLabel?(node, "Category") {
color: #ffd966
color-hover: Darker(#ffd966)
color-selected: #ffd966
}

@NodeStyle HasLabel?(node, "Subcategory") {
color: #ff9100
color-hover: Darker(#ff9100)
color-selected: #ff9100
}

@NodeStyle HasProperty?(node, "name") {
label: AsText(Property(node, "name"))
}

@EdgeStyle {
width: 3
label: Type(edge)
}

@NodeStyle HasLabel?(node, "Company") {
size: 20
color: #FFC500
color-hover: Darker(#FFC500)
color-selected: #FFC500
image-url: Format("https://raw.githubusercontent.com/memgraph/graph-landscape-2022/main/logo/{}.png", LowerCase(Property(node, "img")))
}

```
