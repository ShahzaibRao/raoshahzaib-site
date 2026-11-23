import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// Lazy-load article images (no dependency): every Markdown <img> gets
// loading="lazy" + decoding="async" so long lab articles don't block the
// first paint and off-screen screenshots load only when scrolled to.
function rehypeLazyImages() {
  return (tree) => {
    const visit = (node) => {
      if (node.type === 'element' && node.tagName === 'img') {
        node.properties.loading = 'lazy';
        node.properties.decoding = 'async';
      }
      if (node.children) node.children.forEach(visit);
    };
    visit(tree);
  };
}

export default defineConfig({
  site: 'https://raoshahzaib.site',
  integrations: [sitemap()],
  markdown: {
    rehypePlugins: [rehypeLazyImages],
  },
});
