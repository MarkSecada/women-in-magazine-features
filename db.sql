CREATE TABLE issue_html (
  magazine VARCHAR(32),
  issue_date DATE,
  url TEXT,
  html TEXT
);

CREATE TABLE authors (
  magazine VARCHAR(32),
  issue_date DATE,
  author TEXT
);