-- strip-external-links.lua
-- Pandoc Lua filter for the A5 print export of the book.
--
-- Converts every external link (http/https) into title-only
-- text: the link label is kept, rendered in italics, and the
-- URL is dropped. Full URLs remain available in the online
-- bibliography (Appendix E on the GitHub repository).
-- Internal relative links (chapters, appendices, navigation
-- footers) are left untouched.
--
-- Usage:
--   pandoc ... --lua-filter=tools/strip-external-links.lua

-- -----------------------------------------------------------
--  p r i v a t e
-- -----------------------------------------------------------

-- Check whether a link target points outside the book
local function _isExternal(target)
  return target:match("^https?://") ~= nil
end

-- Extract the host name from a URL (fallback: full target)
local function _hostOf(target)
  return target:match("^https?://([^/]+)") or target
end

-- -----------------------------------------------------------
--  f i l t e r
-- -----------------------------------------------------------

function Link(el)
  if not _isExternal(el.target) then
    -- Keep internal/relative links untouched
    return nil
  end
  local label = pandoc.utils.stringify(el.content)
  local bare = el.target:gsub("^https?://", ""):gsub("/+$", "")
  -- Bare links (label is the URL itself): keep host name only
  if label == el.target or label == bare then
    return pandoc.Emph({ pandoc.Str(_hostOf(el.target)) })
  end
  -- Titled links: keep the title in italics, drop the URL
  return pandoc.Emph(el.content)
end
