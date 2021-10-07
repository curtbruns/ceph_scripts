local function isempty(input)
  return input == nil or input == ''
end

if Request.RGWOp == 'put_obj' then
	RGWDebugLog("Host/Domain/URI/SC for put Host: " .. Request.HTTP.Host .. " Domain: " .. Request.HTTP.Domain .. " URI: " .. Request.HTTP.URI .. " and StorageClass: " .. Request.HTTP.StorageClass )
end

