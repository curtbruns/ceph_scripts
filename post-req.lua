RGWDebugLog("number of metadata entries is: " .. #Request.HTTP.Metadata)
for k, v in pairs(Request.HTTP.Metadata) do
  RGWDebugLog("key=" .. k .. ", " .. "value=" .. v)
--RGWDebugLog("Storage Class Header avail on: " .. Request.Object.Name .. " and storage class: " .. Request.HTTP.Metadata["x-amz-storage-class"])
end

