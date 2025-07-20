-- setup hop
local hop = require'hop'
-- hop.setup { keys = "etovxqpdygfblzhckisuran" }
hop.setup { keys = "asdgqwertyuiopxcvbnmf" }

-- assign hop word highlight to the letter f in all vim modes
vim.keymap.set('', 'f', function()
  hop.hint_words()
end, { remap=true })
