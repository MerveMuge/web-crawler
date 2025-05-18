# Crawler Traversal Strategy: BFS vs DFS

The way a web crawler moves through pages has a major impact on how efficiently it explores a site, how deep it goes, and how well it avoids pitfalls like loops or overload.

This note compares two common strategies — Breadth-First Search (BFS) and Depth-First Search (DFS) — and explains why BFS is used here.

## Why Traversal Strategy Matter

Crawling isn’t just about visiting links — it’s about deciding how to move through the site’s structure. This affects:
- Which pages get visited first
- How far the crawler goes
- HHow much memory it uses
- How to avoid getting stuck in deep or infinite link chains

## Traversal Strategies

### Depth-First Search (DFS)
- DFS goes as far as it can down one path before coming back and trying others.
- **Pros**:
  - Reaches deeply nested pages quickly.
  - Simple to implement with recursion.
- **Cons**:
  - Risk of stack overflow (Python recursion limit).
  - Difficult to enforce a strict depth limit.
  - Can easily get trapped in infinite structures.

### Breadth-First Search (BFS)
- Visits all links at one depth level before going deeper.
- Implemented using a queue (FIFO).
- **Pros**:
  - Easy to track and limit crawl depth.
  - Matches how most websites are structured: homepage → category → content
  - Avoids recursion limits and is safer for large sites.
  - Predictable and easy to test
- **Cons**:
  - Slightly higher memory usage due to queue.
  - Slightly slower in some narrow-depth cases.

## Why I Chose BFS

- Easier to control depth and limit over-fetching
- Matches the way users navigate most websites
- More predictable and reviewable during testing

## Future Improvements

- Add a max_depth setting to stop deep crawls.
- Prioritize certain links (e.g., sitemaps, internal pages)
- Try combining both strategies for different use cases (e.g., DFS for focused discovery, BFS for wide coverage)