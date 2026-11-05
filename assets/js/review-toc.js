
document.addEventListener("DOMContentLoaded", function () {
  const toc = document.getElementById("auto-toc");
  const tocBox = document.getElementById("toc-box");

  if (!toc || !tocBox) return;

  const article = document.querySelector("article");

  if (!article) return;

  const headings = Array.from(
    article.querySelectorAll("h2, h3")
  ).filter(heading => !heading.closest("#toc-box"));

  if (!headings.length) {
    tocBox.style.display = "none";
    return;
  }

  headings.forEach((heading, index) => {
    if (!heading.id) {
      heading.id = "secao-" + (index + 1);
    }

    const li = document.createElement("li");
    const link = document.createElement("a");

    link.href = "#" + heading.id;
    link.textContent = heading.textContent.trim();

    if (heading.tagName === "H3") {
      li.classList.add("toc-subitem");
    }

    li.appendChild(link);
    toc.appendChild(li);
  });
});
