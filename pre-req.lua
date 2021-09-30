if Request.RGWOp == 'put_obj' then
  if (Request.HTTP.Metadata["x-amz-storage-class"] == nil) then
	  RGWDebugLog("No Storage Class Header for this Object put: " .. Request.Object.Name .. " Trying to add QLC_CLASS")
	  Request.HTTP.Metadata["x-amz-storage-class"] = "QLC_CLASS"
  else
	  RGWDebugLog("Storage Class Header avail on: " .. Request.Object.Name .. " and storage class: " .. Request.HTTP.Metadata["x-amz-storage-class"])
  end
--  Request.HTTP.Metadata["x-amz-meta-mydata"] = "my value"
--  RGWDebugLog("good stuff2 x-amz-meta-mydata " .. Request.HTTP.Metadata["x-amz-meta-mydata"] )
end

