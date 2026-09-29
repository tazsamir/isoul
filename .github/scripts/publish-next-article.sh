#!/usr/bin/env bash
set -euo pipefail

section="content/off-the-stack"
order_file="$section/.article_order"

if [[ ! -f "$order_file" ]]; then
  echo "Missing publication order: $order_file" >&2
  exit 1
fi

article_file=""
slug=""
while IFS= read -r candidate; do
  candidate="${candidate#"${candidate%%[![:space:]]*}"}"
  candidate="${candidate%"${candidate##*[![:space:]]}"}"
  [[ -z "$candidate" ]] && continue
  candidate_file="$section/$candidate.md"
  if [[ -f "$candidate_file" ]] && grep -qx 'draft: true' "$candidate_file"; then
    slug="$candidate"
    article_file="$candidate_file"
    break
  fi
done < "$order_file"

if [[ -z "$article_file" ]]; then
  echo "has_article=false" >> "$GITHUB_OUTPUT"
  echo "No draft article remains in the publication queue."
  exit 0
fi

title=$(sed -n 's/^title: *"\(.*\)" *$/\1/p' "$article_file" | head -n 1)
if [[ -z "$title" ]]; then
  echo "Could not read the article title from $article_file" >&2
  exit 1
fi

sed -i '/^draft: true$/d' "$article_file"

next_slug=""
seen_current=false
while IFS= read -r candidate; do
  candidate="${candidate#"${candidate%%[![:space:]]*}"}"
  candidate="${candidate%"${candidate##*[![:space:]]}"}"
  [[ -z "$candidate" ]] && continue
  if [[ "$seen_current" == false ]]; then
    [[ "$candidate" == "$slug" ]] && seen_current=true
    continue
  fi
  candidate_file="$section/$candidate.md"
  if [[ -f "$candidate_file" ]] && grep -qx 'draft: true' "$candidate_file"; then
    next_slug="$candidate"
    break
  fi
done < "$order_file"

{
  echo "has_article=true"
  echo "slug=$slug"
  echo "title=$title"
  echo "article_file=$article_file"
  echo "next_slug=$next_slug"
} >> "$GITHUB_OUTPUT"

printf 'Prepared for publication: %s (%s)\n' "$title" "$slug"
